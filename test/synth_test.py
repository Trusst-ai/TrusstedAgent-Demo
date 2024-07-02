from pydub import AudioSegment
import numpy as np

# Generate a sine wave as an example audio signal
duration = 2.0  # seconds
frequency = 440.0  # Hz
sample_rate = 8000  # 8 kHz
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)

# Convert numpy array to pydub audio segment
audio_segment = AudioSegment(
    (audio_data * 32767).astype(np.int16).tobytes(),
    frame_rate=sample_rate,
    sample_width=2,  # 16-bit audio
    channels=1      # Mono
)

# Export the audio segment to U-Law encoded .wav file
output_filename = 'output_ulaw.wav'
audio_segment.export(output_filename, format='wav', codec='pcm_mulaw')

print(f"File saved as {output_filename}")