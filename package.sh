#! /usr/bin/env bash

sam package \
--template-file lambda.yml \
--output-template-file sam-template.yml \
--s3-bucket whirlwind-packages
