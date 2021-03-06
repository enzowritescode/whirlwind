# Whirlwind

## Overview

This tool utilizes a CloudWatch alarm to trigger a Lambda function. The Lambda function assumes that an elastic IP address is associated to an EC2 instance, with that IP address being attached to an 'A' record on Route53. A new elastic IP address will be allocated, the 'A' record will be updated to point to the new elastic IP address, and the old elastic IP address will be released. If a failure occurs, SNS will push out a notification.

## Requirements
- AWS Serverless Application Model
- Python 3.8
- Boto3
- CodePipeline

## Contents
- template.yml
- config.json
- buildspec.yml
- src/
	- ip_address_changer.py
	- whirlwind.py

## Resources
- [Boto3 - AWS Python SDK](https://aws.amazon.com/sdk-for-python/)
- [CloudFormation](https://aws.amazon.com/cloudformation/)
- [CodePipeline] - https://aws.amazon.com/codepipeline/
- [EC2](https://aws.amazon.com/ec2/)
- [EC2 CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/ec2/)
- [IAM](https://aws.amazon.com/iam/)
- [Route 53](https://aws.amazon.com/ec2/)
- [Route 53 CLI reference](https://docs.aws.amazon.com/cli/latest/reference/route53/)
- [SAM](https://aws.amazon.com/serverless/sam/)
- [SNS](https://aws.amazon.com/sns/)
- Pipeline examples
	- https://github.com/awslabs/aws-sam-codepipeline-cd/blob/master/sam/app/template.yaml
	- https://medium.com/@plourenco/using-codepipeline-to-automate-serverless-applications-deployment-b23e01b15bd1
