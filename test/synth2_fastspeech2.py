import malaya_speech
import malaya
import numpy as np
from malaya_speech import Pipeline
from scipy.signal import resample
from pydub import AudioSegment
import boto3
import time

BUCKET_NAME = 'camilo-sandbox-non-polly-prompts2'
universal_melgan = malaya_speech.vocoder.melgan(model = 'universal-1024')
male_osman = malaya_speech.tts.fastspeech2(model = 'osman')

def write_to_s3(filename):
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=filename,
        Body=open(filename, 'rb')
    )

def generate_tts(text, speed_ratio=1.0):
    start = time.time()
    r_male_osman = male_osman.predict(text, speed_ratio=speed_ratio)
    data = universal_melgan(r_male_osman['universal-output'])
    end = time.time()
    print(f"Prediction duration was {end-start} seconds for text '{text}'")
    return data

def generate_tts_long_text(text, speed_ratio=1.0):
    start = time.time()

    # Define a pipeline that will process each sentence independently
    p = Pipeline()
    pipeline = (
        p.map(malaya.text.function.split_into_sentences)
        .foreach_map(lambda x: male_osman.predict(x, speed_ratio=speed_ratio))
        .foreach_map(lambda x: x['universal-output'])
        .foreach_map(universal_melgan)
    )
    r_male_osman = p(text)

    # Introduce silence between sentences
    silent_period = np.array([0] * int(22050 * 0.5))
    concatenated = []
    for i in range(len(r_male_osman['vocoder-melgan'])):
        c = [r_male_osman['vocoder-melgan'][i]]
        if i < len(r_male_osman['vocoder-melgan']) - 1:
            c.append(silent_period)
        concatenated.extend(c)
    data = np.concatenate(concatenated)

    end = time.time()
    print(f"Prediction duration with speed ration {speed_ratio} was {end-start} seconds for text '{text}'")

    return data


def write_to_fs(output_filename, data):
    start = time.time()
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
    end = time.time()
    print(f"Encoding duration was {end-start} seconds")

    # Export the audio segment to U-Law encoded .wav file
    audio_segment.export(output_filename, format='wav', codec='pcm_mulaw')
    print(f"File saved as {output_filename}")

def prompt_to_file(prompt,filename):
    print(f"Evaluating TTS for file {filename}")

    text = prompt

    # Speed 1.0
    data = generate_tts_long_text(text=text, speed_ratio=1.0)
    output_filename = f"{filename}.wav"
    write_to_fs(output_filename, data)
    write_to_s3(output_filename)

    # Speed 1.0
    slow_data = generate_tts_long_text(text=text, speed_ratio=1.5)
    slow_output_filename = f"{filename}_slow.wav"
    write_to_fs(slow_output_filename, slow_data)
    write_to_s3(slow_output_filename)

# This is James, your personal assistance from Alliance Bank. I will help you change your password. To ensure your privacy and help you effectively, we need to verify you. To proceed with verification, please briefly describe and provide a summary of your most recent interaction with us. Speak clearly and naturally for at least 15 seconds after the tone.
prompt_to_file('Ini James, pembantu peribadi anda dari Alliance Bank. Saya akan membantu anda menukar kata laluan anda. Untuk memastikan privasi anda dan membantu anda dengan berkesan, kami perlu mengesahkan identiti anda. Untuk meneruskan pengesahan, sila huraikan secara ringkas dan berikan ringkasan interaksi terkini anda dengan kami. Bercakaplah dengan jelas dan secara semula jadi selama sekurang-kurangnya 15 saat selepas bunyi isyarat.',
    'prompt_bahasa_1_voiceid')

# Thank you. You successfully authenticated. Please hold for a moment while we proceed to reset your password.
prompt_to_file('Terima kasih. Anda berjaya mengesahkan. Sila tahan seketika sementara kami meneruskan untuk menetapkan semula kata laluan anda.',
    'prompt_bahasa_2_resetting_password')

# Your password has been successfully reset. Is there anything else I can assist you with today?
prompt_to_file('Kata laluan anda telah berjaya ditetapkan semula. Adakah terdapat apa-apa lagi yang boleh saya bantu anda hari ini?',
    'prompt_bahasa_3_anything_else')

# Unfortunately, there was an error. Please try again later.
prompt_to_file('Malangnya, terdapat ralat. Sila cuba sebentar lagi.',
    'prompt_bahasa_4_unfortunately_error')

# I encountered an error! Goodbye!
prompt_to_file('Saya mengalami ralat! selamat tinggal!.',
    'prompt_bahasa_5_error_goodbye')

# That concludes the test. Thank you, goodbye!
prompt_to_file('Itu menyimpulkan ujian. Terima kasih selamat tinggal!',
    'prompt_bahasa_5_concludes_goodbye')

# Roger that, I'm just thinking, hang on.
prompt_to_file('Roger itu, saya hanya berfikir, tahan.',
    'prompt_bahasa_6_roger_that')

# Cool, I'm just looking that up.
prompt_to_file('Hebat, saya hanya melihatnya.',
    'prompt_bahasa_7_cool_looking_up')

# Thanks! I won't be a second.
prompt_to_file('Terima kasih! Saya tidak akan menjadi kedua.',
    'prompt_bahasa_8_thanks_second')

# I'm just finding the best solution for that.
prompt_to_file('Saya hanya mencari penyelesaian terbaik untuk itu.',
    'prompt_bahasa_9_best_solution')

# Cool. Won't be long.
prompt_to_file('Sejuk. Tidak lama lagi.',
    'prompt_bahasa_10_cool_wont')

# I am enabling thinking mode.
prompt_to_file('Saya mendayakan mod berfikir.',
    'prompt_bahasa_11_enable_thinking')

# Welcome!
prompt_to_file('Selamat datang',
    'prompt_bahasa_12_welcome')

# Unfortunately there was an error. You will now be transferred to our next available agent to authenticate you or enroll your Voice ID.
prompt_to_file('Malangnya terdapat ralat. Anda kini akan dipindahkan ke ejen kami yang tersedia seterusnya untuk mengesahkan anda atau mendaftarkan ID Suara anda.',
    'prompt_bahasa_13_enroll')

# Thank you. A one-time password has been sent via SMS. Please enter the PIN using your keypad after the beep.
prompt_to_file('Terima kasih. Kata laluan sekali guna telah dihantar melalui SMS. Sila masukkan PIN menggunakan pad kekunci anda selepas bunyi bip.',
    'prompt_bahasa_14_one_time_password_sent')

# Thank you. You have been successfully authenticated using voice biometrics and a one-time PIN. Please wait while we reset your password.
prompt_to_file('Terima kasih. Anda telah berjaya disahkan menggunakan biometrik suara dan PIN sekali guna. Sila tunggu sementara kami menetapkan semula kata laluan anda.',
    'prompt_bahasa_15_successfully_authenticated')

# Sorry, we didn't recognise your input, please try entering the one time pin again. 
prompt_to_file('Maaf, kami tidak dapat mengenali input anda. Sila cuba masukkan PIN sekali guna sekali lagi.',
    'prompt_bahasa_16_input_not_recognised')

# You have exceeded the number of retry attempts.
prompt_to_file('Anda telah melebihi bilangan percubaan yang dibenarkan.',
    'prompt_bahasa_17_retries_exceeded')

# Your password has been reset successfully.
prompt_to_file('Kata laluan anda telah berjaya ditetapkan semula.',
    'prompt_bahasa_18_password_reset_successful')