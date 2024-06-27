#!/bin/bash -xe

# The chosen image doesn't have Amazon EFS utils installed and thus it needs to be installed .
# mkdir -p /mnt/efs # Seems like not enough perms to do this
sudo apt-get -y update
sudo apt-get -y install git binutils rustc cargo pkg-config libssl-dev

cd /home/ubuntu
MAIN_DIRECTORY=/home/ubuntu
# if [ ! -d "/mnt/efs/python-env" ]; then

sudo apt-get -y upgrade
sudo apt-get install -y --no-install-recommends ffmpeg
sudo apt-get install -y git
sudo apt-get install -y python3-virtualenv
echo "Creating Python environment"
/opt/conda/bin/python -m venv ${MAIN_DIRECTORY}/python-venv
source ${MAIN_DIRECTORY}/python-venv/bin/activate
pip install pandas requests
pip install torch==2.0.0
pip install torchaudio==2.0.0
pip install torchvision
pip install pysoundfile
pip install ffmpeg
pip install pydub
pip install anthropic[bedrock]
# pip install git+https://github.com/m-bain/whisperx.git
# sudo aws s3 cp s3://${BUCKET_NAME}/trusstpy-0.0.1.tar.gz .
# pip install trusstpy-0.0.1.tar.gz
pip install boto3
pip install numpy==1.26.4

# dependencies for flask application
pip install flask
pip install tortoise-tts

# else
#     echo "Python environment Already Exists, starting environment"
#     source /mnt/efs/python-env/bin/activate
# fi

export AWS_DEFAULT_REGION=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone | sed 's/\(.*\)[a-z]/\1/')
mkdir -p ~/.aws
echo -e "[default]\nregion=${AWS_DEFAULT_REGION}" > ~/.aws/config

python <<HEREDOC
from trusstpy.server import server
server()
HEREDOC