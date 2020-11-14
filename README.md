# Whirlwind

## Backstory

This tool was originally developed with a VPN server in mind. The objective was to rotate the IP address of a VPN server and then update the corresponding DNS records.

## Description

This tool currently only works with Amazon Web Services (AWS). An elastic IP address should be associated to an EC2 instance, with that IP address being attached to an 'A' record on Route53. A new elastic IP address will be allocated, the 'A' record will be updated to point to the new elastic IP address, and the old elastic IP address will be released. If a failure occurs, SNS will push out a notification. 

## Requirements
- AWS Serverless Application Model (SAM) CLI
- Python 3.8
- Boto3

## Contents
- deploy.sh
- package.sh
- lambda.yml
- src/
	- ip_address_changer.py
	- whirlwind.py

## Resources
- [Boto3 - AWS Python SDK](https://aws.amazon.com/sdk-for-python/)
- [EC2](https://aws.amazon.com/ec2/)
- [EC2 CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/ec2/)
- [IAM](https://aws.amazon.com/iam/)
- [Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
- [Route 53](https://aws.amazon.com/ec2/)
- [Route 53 CLI reference](https://docs.aws.amazon.com/cli/latest/reference/route53/)
- [SAM](https://aws.amazon.com/serverless/sam/)
- [SNS](https://aws.amazon.com/sns/)
