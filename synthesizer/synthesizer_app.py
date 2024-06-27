from flask import Flask, request, jsonify, send_file
import os
import uuid
import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F
from tortoise.api_fast import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices

import numpy as np
import io


app = Flask(__name__)

tts = TextToSpeech(use_deepspeed=True, kv_cache=True, half=True)

# Pick one of the voices from the output above
voice = 'emma'

# Load it and send it through Tortoise.
voice_samples, conditioning_latents = load_voice(voice)


@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    gen = tts.tts(text, voice_samples=voice_samples, conditioning_latents=conditioning_latents)
    
    buffer = io.BytesIO()
    np.save(buffer, gen.squeeze(0).cpu().numpy())
    buffer.seek(0)
    
    
    # Send the file object as the response
    return send_file(
        buffer,
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name='audio.bin'  # Specify the desired file name for the download
    )

"""
usage
import requests
import io
import numpy as np

url = 'http://localhost:5000/synthesize'
data = {
    "text": "[why are you asking me some dumb fucking questions]"
}

response = requests.post(url, json=data)



buffer = io.BytesIO(response.content)
audio_array = np.load(buffer)

from IPython.display import Audio, display

# Create an Audio widget
audio_widget = Audio(data=audio_array, rate=22000)  # Replace 22050 with the actual sample rate of your audio

# Display the Audio widget
display(audio_widget)

"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    