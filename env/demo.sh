#!/bin/bash

# Change to test, uat, prod etc
export stage=demo

# Should not need to change
export service=trusstedagent

# Target AWS deployment region
export region=ap-southeast-1

# Bedrock region
export bedrockRegion=ap-southeast-2

export AWS_REGION=$region

export AWS_PROFILE=alliance

if [ -z "$AWS_PROFILE" ]; then
  echo "Please set AWS_PROFILE=<<your-aws-profile>> before continuing..."
  exit 1
fi

echo "Using AWS_PROFILE=${AWS_PROFILE}"

# AWS account number
export accountNumber=$(aws sts get-caller-identity --query Account --output text)

# Whisper V3
export whisperEndPoint=lissten-malay

# S3 bucket to upload deployment assets to
export deploymentBucket="${stage}-${service}-deployment-${accountNumber}"

echo "Exported $stage"
