import malaya_speech
import numpy as np
from malaya_speech import Pipeline
from scipy.signal import resample
from pydub import AudioSegment
import boto3

def write_to_s3(filename):
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket='alliance-bank-non-polly-prompts',
        Key=filename,
        Body=open(filename, 'rb')
    )

def prompt_to_file(prompt,filename):
    universal_melgan = malaya_speech.vocoder.melgan(model = 'universal-384')
    male_tacotron2 = malaya_speech.tts.tacotron2(model = 'osman')

    text = prompt

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
    output_filename = filename
    audio_segment.export(output_filename, format='wav', codec='pcm_mulaw')

    print(f"File saved as {output_filename}")

    write_to_s3(output_filename)

# This is James, your personal assistant from Alliance Bank. I will help you change your password. To ensure your privacy and help you effectively, we need to verify you. To proceed with verification, please briefly describe and provide a summary of your most recent interactions with us. Speak clearly and naturally for at least 15 seconds after the tone.
prompt_to_file('Ini James, pembantu Maya dari Alliance Bank. Saya akan membantu anda menukar kata laluan anda. Untuk memastikan privasi anda dan membantu anda dengan berkesan, kami perlu mengesahkan anda. Untuk meneruskan dengan pengesahan, sila terangkan secara ringkas dan berikan ringkasan interaksi terbaharu anda dengan kami. Bercakap dengan jelas dan semula jadi selama sekurang-kurangnya 15 saat selepas nada.',
    'prompt_bahasa_1_voiceid.wav')

# Thank you. You successfully authenticated. Please hold for a moment while we proceed to reset your password.
prompt_to_file('Terima kasih. Anda berjaya mengesahkan. Sila tahan seketika sementara kami meneruskan untuk menetapkan semula kata laluan anda.',
    'prompt_bahasa_2_resetting_password.wav')

# Your password has been successfully reset. Is there anything else I can assist you with today?
prompt_to_file('Kata laluan anda telah berjaya ditetapkan semula. Adakah terdapat apa-apa lagi yang boleh saya bantu anda hari ini?',
    'prompt_bahasa_3_anything_else.wav')

# Unfortunately, there was an error. Please try again later.
prompt_to_file('Malangnya, terdapat ralat. Sila cuba sebentar lagi.',
    'prompt_bahasa_4_unfortunately_error.wav')

# I encountered an error! Goodbye!
prompt_to_file('Saya mengalami ralat! selamat tinggal!.',
    'prompt_bahasa_5_error_goodbye.wav')

# That concludes the test. Thank you, goodbye!
prompt_to_file('Itu menyimpulkan ujian. Terima kasih selamat tinggal!',
    'prompt_bahasa_5_concludes_goodbye.wav')

# Roger that, I'm just thinking, hang on.
prompt_to_file('Roger itu, saya hanya berfikir, tahan.',
    'prompt_bahasa_6_roger_that.wav')

# Cool, I'm just looking that up.
prompt_to_file('Hebat, saya hanya melihatnya.',
    'prompt_bahasa_7_cool_looking_up.wav')

# Thanks! I won't be a second.
prompt_to_file('Terima kasih! Saya tidak akan menjadi kedua.',
    'prompt_bahasa_8_thanks_second.wav')

# I'm just finding the best solution for that.
prompt_to_file('Saya hanya mencari penyelesaian terbaik untuk itu.',
    'prompt_bahasa_9_best_solution.wav')

# Cool. Won't be long.
prompt_to_file('Sejuk. Tidak lama lagi.',
    'prompt_bahasa_10_cool_wont.wav')

# I am enabling thinking mode.
prompt_to_file('Saya mendayakan mod berfikir.',
    'prompt_bahasa_11_enable_thinking.wav')

# Welcome!
prompt_to_file('Selamat datang',
    'prompt_bahasa_12_welcome.wav')

# Unfortunately there was an error. You will now be transferred to our next available agent to authenticate you or enroll your Voice ID.
prompt_to_file('Malangnya terdapat ralat. Anda kini akan dipindahkan ke ejen kami yang tersedia seterusnya untuk mengesahkan anda atau mendaftarkan ID Suara anda.',
    'prompt_bahasa_13_enroll.wav')

