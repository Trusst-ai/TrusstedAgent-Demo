rom flask import Flask, request, jsonify, send_file, make_response
import boto3

import malaya_speech
import numpy as np
from malaya_speech import Pipeline
from scipy.signal import resample
from pydub import AudioSegment

app = Flask(__name__)

universal_melgan = malaya_speech.vocoder.melgan(model = 'universal-384')
male_tacotron2 = malaya_speech.tts.tacotron2(model = 'osman')

bucketName = 'demo-trusstedagent-deployment-471112788437'
audioFileName = 'file.wav'

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    r_male_tacotron2 = male_tacotron2.predict(text)
    data = universal_melgan(r_male_tacotron2['universal-output'])

    sample_rate_original = 22050
    sample_rate_target = 8000
    number_of_samples = round(len(data) * float(sample_rate_target) / sample_rate_original)
    audio_data_8000 = resample(data, number_of_samples)

    # Convert numpy array to pydub audio segment
    audio_segment = AudioSegment(
        (audio_data_8000 * 32767).astype(np.int16).tobytes(),
        frame_rate=sample_rate_target,
        sample_width=2,  # 16-bit audio
        channels=1      # Mono
    )

    # Export the audio segment to U-Law encoded .wav file
    output_filename = audioFileName
    audio_segment.export(output_filename, format='wav', codec='pcm_mulaw')

    write_to_s3(data)

    return make_response(jsonify({'success':True}), 200)

def write_to_s3(data):
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=bucketName,
        Key=audioFileName,
        Body=open(audioFileName, 'rb')
    )
    # s3.Object(bucketName, audioFileName).put(Body=open(audioFileName, 'rb'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)