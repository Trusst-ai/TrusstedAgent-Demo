#!/bin/bash

# Change to test, uat, prod etc
export stage=dev

# Should not need to change
export service=trusstedagent

# Target AWS deployment region
export region=ap-southeast-2

# Bedrock region
export bedrockRegion=ap-southeast-2

export AWS_REGION=$region

export profile=camilo-sandbox
export AWS_PROFILE=$profile

echo "Enabled AWS_PROFILE = $AWS_PROFILE"

# AWS account number
export accountNumber=$(aws sts get-caller-identity --query Account --output text)

# Whisper V3
export whisperEndPoint=whisper-endpoint

# S3 bucket to upload deployment assets to
export deploymentBucket="${stage}-${service}-deployment-${accountNumber}"

echo "Exported $stage"
