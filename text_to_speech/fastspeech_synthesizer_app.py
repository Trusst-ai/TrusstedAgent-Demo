from flask import Flask, request, jsonify, send_file, make_response
import os
import uuid
import io
import boto3

import malaya_speech
import numpy as np
from malaya_speech import Pipeline
import matplotlib.pyplot as plt
import IPython.display as ipd
import soundfile as sf

app = Flask(__name__)

universal_melgan = malaya_speech.vocoder.melgan(model = 'universal-384')
male_tacotron2 = malaya_speech.tts.tacotron2(model = 'osman')

bucketName = 'trussted-agent-text-to-speech-bucket'
audioFileName = 'file.wav'

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    r_male_tacotron2 = male_tacotron2.predict(text)
    data = universal_melgan(r_male_tacotron2['universal-output'])
    
    # Write to local system (we'll buffer it into S3)
    write_to_local_fs(data)
    write_to_s3(data)

    return make_response(jsonify({'success':True}), 200)

def write_to_local_fs(data):
    sf.write(audioFileName, data, 22050)

def write_to_s3(data):
    s3 = boto3.client("s3")
    s3.Object(bucketName, audioFileName).put(Body=open(audioFileName, 'rb'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)