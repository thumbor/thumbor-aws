#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com


from thumbor.config import Config, config

import thumbor_aws.loader  # noqa pylint: disable=import-error,unused-import,no-name-in-module
import thumbor_aws.result_storage  # noqa pylint: disable=import-error,unused-import,no-name-in-module
import thumbor_aws.storage  # noqa pylint: disable=import-error,unused-import,no-name-in-module

Config.define(
    "AWS_DEFAULT_LOCATION",
    "https://{bucket_name}.s3.amazonaws.com",
    (
        "Default location to use if S3 does not return location header."
        " Can use {bucket_name} var."
    ),
    "AWS Storage",
)

# TC_AWS Compatibility settings
Config.define(
    "RUN_IN_COMPATIBILITY_MODE",
    False,
    "Runs in compatibility mode using the configurations for tc_aws.",
    "tc_aws Compatibility",
)

Config.define(
    "TC_AWS_REGION",
    "us-east-1",
    "AWS Region the bucket is located in.",
    "tc_aws Compatibility",
)


def __generate_config():
    config.generate_config()


if __name__ == "__main__":
    __generate_config()
