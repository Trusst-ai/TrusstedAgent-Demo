from flask import Flask, request, jsonify, send_file, make_response
import boto3

import malaya_speech
import numpy as np
from malaya_speech import Pipeline
from scipy.signal import resample
from pydub import AudioSegment
import time

app = Flask(__name__)

universal_melgan = malaya_speech.vocoder.melgan(model="universal-384")
male_tacotron2 = malaya_speech.tts.tacotron2(model="yasmin")

bucketName = "demo-trusstedagent-deployment-471112788437"
audioFileName = "file.wav"


def write_to_s3(bucket_name, filename):
    start = time.time()

    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=bucket_name,
        Key=filename,
        Body=open(filename, "rb"),
    )

    end = time.time()
    print(f"S3 upload took {end-start} seconds for file {filename}")


def generate_tts_long_text(text, speed_ratio=1.0):
    start = time.time()

    # Define a pipeline that will process each sentence independently
    p = Pipeline()
    pipeline = (
        p.map(malaya.text.function.split_into_sentences)
        .foreach_map(lambda x: male_osman.predict(x, speed_ratio=speed_ratio))
        .foreach_map(lambda x: x["universal-output"])
        .foreach_map(universal_melgan)
    )
    r_male_osman = p(text)

    # Introduce silence between sentences
    silent_period = np.array([0] * int(22050 * 0.5))
    concatenated = []
    for i in range(len(r_male_osman["vocoder-melgan"])):
        c = [r_male_osman["vocoder-melgan"][i]]
        if i < len(r_male_osman["vocoder-melgan"]) - 1:
            c.append(silent_period)
        concatenated.extend(c)
    data = np.concatenate(concatenated)

    end = time.time()
    print(
        f"Prediction duration with speed ration {speed_ratio} was {end-start} seconds for text '{text}'"
    )

    return data


def write_to_fs(output_filename, data):
    start = time.time()
    sample_rate_original = 22050
    sample_rate_target = 8000
    number_of_samples = round(
        len(data) * float(sample_rate_target) / sample_rate_original
    )
    audio_data_8000 = resample(data, number_of_samples)

    # Convert numpy array to pydub audio segment
    audio_segment = AudioSegment(
        (audio_data_8000 * 32767).astype(np.int16).tobytes(),
        frame_rate=sample_rate_target,
        sample_width=2,  # 16-bit audio
        channels=1,  # Mono
    )
    end = time.time()
    print(f"Encoding duration was {end-start} seconds")

    # Export the audio segment to U-Law encoded .wav file
    audio_segment.export(output_filename, format="wav", codec="pcm_mulaw")
    print(f"File saved as {output_filename}")


def prompt_to_file(prompt, filename):
    print(f"Evaluating TTS for file {filename}")

    text = prompt

    # Speed 1.0
    data = generate_tts_long_text(text=text, speed_ratio=1.0)
    write_to_fs(filename, data)
    write_to_s3(filename)


@app.route("/synthesize", methods=["POST"])
def synthesize():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    r_male_tacotron2 = male_tacotron2.predict(text)
    data = universal_melgan(r_male_tacotron2["universal-output"])

    sample_rate_original = 22050
    sample_rate_target = 8000
    number_of_samples = round(
        len(data) * float(sample_rate_target) / sample_rate_original
    )
    audio_data_8000 = resample(data, number_of_samples)

    # Convert numpy array to pydub audio segment
    audio_segment = AudioSegment(
        (audio_data_8000 * 32767).astype(np.int16).tobytes(),
        frame_rate=sample_rate_target,
        sample_width=2,  # 16-bit audio
        channels=1,  # Mono
    )

    # Export the audio segment to U-Law encoded .wav file
    output_filename = audioFileName
    audio_segment.export(output_filename, format="wav", codec="pcm_mulaw")

    write_to_s3(data)

    return make_response(jsonify({"success": True}), 200)


def write_to_s3(data):
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucketName, Key=audioFileName, Body=open(audioFileName, "rb"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)
