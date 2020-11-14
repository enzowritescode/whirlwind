#! /usr/bin/env bash

sam deploy \
--template-file sam-template.yml \
--stack-name whirlwind \
--capabilities CAPABILITY_NAMED_IAM
