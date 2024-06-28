#!/bin/bash

# Change to test, uat, prod etc
export stage=dev

# Should not need to change
export service=connectvoice

# Target AWS deployment region
export region=us-west-2

# Bedrock region
export bedrockRegion=us-west-2

export AWS_REGION=$region

if [ -z "$AWS_PROFILE" ]; then
  echo "Please set AWS_PROFILE=<<your-aws-profile>> before continuing..."
  exit 1
fi

# AWS account number
export accountNumber=$(aws sts get-caller-identity --query Account --output text)

# Whisper V3
export whisperEndPoint=whisper-endpoint

# S3 bucket to upload deployment assets to
export deploymentBucket="${stage}-${service}-deployment-${accountNumber}"

echo "Exported $stage"
