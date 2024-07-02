import malaya_speech
import numpy as np
from malaya_speech import Pipeline
from scipy.signal import resample
from pydub import AudioSegment


universal_melgan = malaya_speech.vocoder.melgan(model = 'universal-384')
male_tacotron2 = malaya_speech.tts.tacotron2(model = 'osman')

audioFileName = 'output_ulaw.wav'

text = 'Ini adalah ayat bahasa terbaik yang pernah saya katakan'

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
output_filename = 'output_ulaw.wav'
audio_segment.export(output_filename, format='wav', codec='pcm_mulaw')

print(f"File saved as {output_filename}")