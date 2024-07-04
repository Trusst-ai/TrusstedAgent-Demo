#!/bin/bash -xe

sudo apt-get -y update
sudo apt-get -y install git binutils rustc cargo pkg-config libssl-dev

MAIN_DIRECTORY=/home/ubuntu
cd ${MAIN_DIRECTORY}

sudo apt-get -y upgrade
sudo apt-get install -y --no-install-recommends ffmpeg
sudo apt-get install -y git
sudo apt-get install -y python3-virtualenv
echo "Creating and activating Python environment"
/opt/conda/bin/python -m venv ${MAIN_DIRECTORY}/python-venv
source ${MAIN_DIRECTORY}/python-venv/bin/activate
echo "Installing dependencies"
pip install pandas requests
pip install torch==2.1.0
pip install torchaudio==2.0.0
pip install torchvision
pip install pysoundfile
pip install ffmpeg
pip install pydub
pip install anthropic[bedrock]
pip install boto3
pip install numpy==1.26.4
pip install flask

# dependencies for text-to-speech using tortoise
# pip install tortoise-tts

# dependencies for flask application using FastSpeech
# echo "Installing dependencies for FastSpeech text-to-speech"
pip install malaya-speech

# tensorflow and tensorflow-estimator must have a matching version
# https://stackoverflow.com/questions/66022256/modulenotfounderror-no-module-named-tensorflow-core-estimator-for-tensorflow
pip install tensorflow==2.15.0
pip install tensorrt
pip install tensorflow-estimator==2.15.0
pip install malaya
pip install matplotlib
pip install ipython
pip install BeautifulSoup4

python <<HEREDOC
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
    s3.put_object(
        Bucket=bucketName,
        Key=audioFileName,
        Body=open(audioFileName, 'rb')
    )

if __name__ == '__main__':
    # App must run on port 80 so it can be reached from outside the Default VPN
    app.run(host='0.0.0.0', port=80)
HEREDOC