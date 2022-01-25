#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com


from thumbor.config import Config, config

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
    "THUMBOR_AWS_RUN_IN_COMPATIBILITY_MODE",
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

# TODO: Support retries
Config.define(
    "TC_AWS_MAX_RETRY",
    0,
    "Max retries for get image from S3 Bucket. Default is 0",
    "tc_aws Compatibility",
)

# TC_AWS Loader Settings

Config.define(
    "TC_AWS_LOADER_BUCKET",
    "",
    "S3 bucket for Loader. If given, source urls are interpreted as keys "
    "within this bucket. If not given, source urls are expected to contain"
    "the bucket name, such as 's3-bucket/keypath'.",
    "tc_aws Compatibility",
)

Config.define(
    "TC_AWS_LOADER_ROOT_PATH",
    "",
    "S3 path prefix for Loader bucket. "
    "If given, this is prefixed to all S3 keys.",
    "tc_aws Compatibility",
)

# TC_AWS Storage Settings

Config.define(
    "TC_AWS_STORAGE_BUCKET",
    "",
    "S3 bucket for Storage",
    "tc_aws Compatibility",
)

Config.define(
    "TC_AWS_STORAGE_ROOT_PATH",
    "",
    "S3 path prefix for Storage bucket",
    "tc_aws Compatibility",
)

# TODO: Support SSE
Config.define(
    "TC_AWS_STORAGE_SSE",
    False,
    "put data into S3 using the Server Side Encryption functionality to "
    "encrypt data at rest in S3 "
    "https://aws.amazon.com/about-aws/whats-new"
    "/2011/10/04/amazon-s3-announces-server-side-encryption-support/",
    "tc_aws Compatibility",
)

# TODO: Support RRS
Config.define(
    "TC_AWS_STORAGE_RRS",
    False,
    "put data into S3 with Reduced Redundancy "
    "https://aws.amazon.com/about-aws/whats-new"
    "/2010/05/19/announcing-amazon-s3-reduced-redundancy-storage/",
    "tc_aws Compatibility",
)

# Result Storage

Config.define(
    "TC_AWS_RESULT_STORAGE_BUCKET",
    "",
    "S3 bucket for result Storage",
    "tc_aws Compatibility",
)

Config.define(
    "TC_AWS_RESULT_STORAGE_ROOT_PATH",
    "",
    "S3 path prefix for Result storage bucket",
    "tc_aws Compatibility",
)

# Thumbor AWS already does this
Config.define(
    "TC_AWS_STORE_METADATA",
    False,
    "Store result with metadata (for instance content-type)",
    "tc_aws Compatibility",
)


def __generate_config():
    config.generate_config()


if __name__ == "__main__":
    __generate_config()
