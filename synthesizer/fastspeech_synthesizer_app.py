from flask import Flask, request, jsonify, send_file, make_response
import os
import uuid
import io

import malaya_speech
import numpy as np
from malaya_speech import Pipeline
import matplotlib.pyplot as plt
import IPython.display as ipd
import soundfile as sf

app = Flask(__name__)

universal_melgan = malaya_speech.vocoder.melgan(model = 'universal-384')
male_tacotron2 = malaya_speech.tts.tacotron2(model = 'osman')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    r_male_tacotron2 = male_tacotron2.predict(text)
    data = universal_melgan(r_male_tacotron2['universal-output'])
    
    # TODO: Send file over to S3 bucket
    sf.write('file.wav', data, 22050)

    return make_response(jsonify({'success':True}), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)