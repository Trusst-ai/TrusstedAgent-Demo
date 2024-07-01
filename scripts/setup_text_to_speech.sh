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
pip install "tensorflow==2.15.0"
pip install tensorrt
pip install "tensorflow-estimator==2.15.0"
pip install malaya
pip install matplotlib
pip install ipython
pip install BeautifulSoup4

# python <<HEREDOC
# from trusstpy.server import server
# server()
# HEREDOC