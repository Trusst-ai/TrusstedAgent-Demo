import malaya_speech
import numpy as np
from malaya_speech import Pipeline
from scipy.signal import resample
from pydub import AudioSegment
import boto3


def write_to_s3(filename):
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket="alliance-bank-non-polly-prompts",
        Key=filename,
        Body=open(filename, "rb"),
    )


def prompt_to_file(prompt, filename):
    universal_melgan = malaya_speech.vocoder.melgan(model="universal-384")
    male_tacotron2 = malaya_speech.tts.tacotron2(model="osman")

    text = prompt

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
    output_filename = filename
    audio_segment.export(output_filename, format="wav", codec="pcm_mulaw")

    print(f"File saved as {output_filename}")

    write_to_s3(output_filename)


# 1 Thank you for contacting Alliance Bank. My name is Maya, and I will assist you today. For security purposes, I need you to speak clearly and repeat a short phrase to verify your identity. The phrase to be repeated is: 'My bank information is sensitive. I will not download any APK files. I will not click any links in SMS.' Please repeat this phrase to the best of your ability after the beep.
prompt_to_file(
    'Terima kasih kerana menghubungi Allaiance Bank. Nama saya Ari, dan saya akan membantu anda pada hari ini. Untuk tujuan keselamatan, saya memerlukan anda untuk bercakap dengan jelas dan mengulangi frasa pendek bagi mengesahkan aidentiti anda. Frasa yang perlu diulangi ialah: "Maklumat bank saya adalah sensitif. Saya tidak akan memuat turun sebarang fail aipikei. Saya tidak akan mengklik sebarang pautan dalam SMS." Sila ulang frasa ini sebaik mungkin selepas bunyi bip',
    "prompt_bahasa_1_voiceid.wav",
)

# 2 Thank you. You successfully authenticated. Please hold for a moment while we proceed to reset your password"
prompt_to_file(
    "Terima kasih. Anda telah berjaya mengesahkan identiti anda. Sila tunggu sebentar sementara kami mengemaskini kata laluan anda.",
    "prompt_bahasa_2_resetting_password.wav",
)

# 3 "Your password has been successfully reset. Is there anything else I can assist you with today?"
prompt_to_file(
    "Kata laluan anda telah dikemaskini. Ada apa-apa yang saya bantu anda hari ini?",
    "prompt_bahasa_3_anything_else.wav",
)

# 4 Unfortunately, there was an error. Please try again later.
prompt_to_file(
    "Harap maaf, sila cuba sekali lagi", "prompt_bahasa_4_unfortunately_error.wav"
)

# 5 Unfortunately, we are unable to authenticate you. We will transfer you to our agent for verification.
prompt_to_file(
    "Harap maaf, kami tidak dapat mengesahkan identiti anda. Kami akan memindahkan anda kepada ejen kami untuk pengesahan.",
    "prompt_bahasa_5_error_goodbye.wav",
)

# That concludes the test. Thank you, goodbye!
prompt_to_file(
    "Itu menyimpulkan ujian. Terima kasih selamat tinggal!",
    "prompt_bahasa_5_concludes_goodbye.wav",
)

# Thank you, one moment please.
prompt_to_file(
    "Baiklah. Tidak akan mengambil masa yang lama.", "prompt_bahasa_6_roger_that.wav"
)

# Thank you, please hold on
prompt_to_file(
    "Terima kasih, sila tunggu sebentar", "prompt_bahasa_7_cool_looking_up.wav"
)

# Thank you, please hold on
prompt_to_file(
    "Terima kasih, sila tunggu sebentar", "prompt_bahasa_8_thanks_second.wav"
)

# Thank you, please hold on
prompt_to_file(
    "Terima kasih, sila tunggu sebentar", "prompt_bahasa_9_best_solution.wav"
)

# Thank you, please hold on
prompt_to_file("Terima kasih, sila tunggu sebentar", "prompt_bahasa_10_cool_wont.wav")

# I am enabling thinking mode.
prompt_to_file("Saya mendayakan mod berfikir.", "prompt_bahasa_11_enable_thinking.wav")

# Welcome!
prompt_to_file("Selamat datang", "prompt_bahasa_12_welcome.wav")

# Unfortunately, we are unable to authenticate you. We will transfer you to our agent for verification.
prompt_to_file(
    "Harap maaf, kami tidak dapat mengesahkan identiti anda. Kami akan memindahkan anda kepada ejen kami untuk pengesahan.",
    "prompt_bahasa_13_enroll.wav",
)

# Thank you. A one-time password has been sent via SMS. Please enter the PIN using your keypad after the beep.
# N/A: We've disabled MFA
prompt_to_file(
    "Terima kasih. Kata laluan sekali guna telah dihantar melalui SMS. Sila masukkan PIN menggunakan pad kekunci anda selepas bunyi bip.",
    "prompt_bahasa_14_one_time_password_sent.wav",
)

# Thank you. You have been successfully authenticated using voice biometrics and a one-time PIN. Please wait while we reset your password.
# N/A: We've disabled MFA
prompt_to_file(
    "Terima kasih. Anda telah berjaya disahkan menggunakan biometrik suara dan PIN sekali guna. Sila tunggu sementara kami menetapkan semula kata laluan anda.",
    "prompt_bahasa_15_successfully_authenticated.wav",
)

# Sorry, we didn't recognise your input, please try entering the one time pin again.
# N/A: We've disabled MFA
prompt_to_file(
    "Maaf, kami tidak dapat mengenali input anda. Sila cuba masukkan PIN sekali guna sekali lagi.",
    "prompt_bahasa_16_input_not_recognised.wav",
)

# You have exceeded the number of retry attempts.
prompt_to_file(
    "Anda telah melebihi bilangan percubaan yang dibenarkan.",
    "prompt_bahasa_17_retries_exceeded.wav",
)

# Your password has been reset successfully.
prompt_to_file(
    "Kata laluan anda telah dikemaskini",
    "prompt_bahasa_18_password_reset_successful.wav",
)

# Thank you for contacting Alliance Bank. We hope you are satisfied with our service.
prompt_to_file(
    "Terima kasih kerana menghubungi Alliance Bank. Kami berharap anda berpuas hati dengan perkhidmatan kami.",
    "prompt_bahasa_19_satisfied_service.wav",
)
