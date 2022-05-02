#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com


from thumbor.loaders import LoaderResult

from thumbor_aws.config import Config
from thumbor_aws.s3_client import S3Client

Config.define(
    "AWS_LOADER_REGION_NAME",
    "us-east-1",
    "Region where thumbor's objects are going to be loaded from.",
    "AWS Loader",
)

Config.define(
    "AWS_LOADER_BUCKET_NAME",
    "thumbor",
    "S3 Bucket where thumbor's objects are loaded from.",
    "AWS Loader",
)

Config.define(
    "AWS_LOADER_S3_SECRET_ACCESS_KEY",
    None,
    "Secret access key for S3 Loader.",
    "AWS Loader",
)

Config.define(
    "AWS_LOADER_S3_ACCESS_KEY_ID",
    None,
    "Access key ID for S3 Loader.",
    "AWS Loader",
)

Config.define(
    "AWS_LOADER_S3_ENDPOINT_URL",
    None,
    "Endpoint URL for S3 API. Very useful for testing.",
    "AWS Loader",
)

Config.define(
    "AWS_LOADER_ROOT_PATH",
    "/st",
    "Loader prefix path.",
    "AWS Loader",
)


async def load(context, path):
    """Loader to get source files from S3"""
    client = S3Client(context)
    client.configuration = {
        "region_name": context.config.AWS_LOADER_REGION_NAME,
        "secret_access_key": context.config.AWS_LOADER_S3_SECRET_ACCESS_KEY,
        "access_key_id": context.config.AWS_LOADER_S3_ACCESS_KEY_ID,
        "endpoint_url": context.config.AWS_LOADER_S3_ENDPOINT_URL,
        "bucket_name": context.config.AWS_LOADER_BUCKET_NAME,
        "root_path": context.config.AWS_LOADER_ROOT_PATH,
    }
    if client.compatibility_mode is True:
        client.configuration["region_name"] = context.config.TC_AWS_REGION
        client.configuration["endpoint_url"] = context.config.TC_AWS_ENDPOINT
        client.configuration[
            "bucket_name"
        ] = context.config.TC_AWS_LOADER_BUCKET
        client.configuration[
            "root_path"
        ] = context.config.TC_AWS_LOADER_ROOT_PATH

    bucket, real_path = get_bucket_and_path(
        client.configuration["bucket_name"], path
    )

    norm_path = normalize_url(client.configuration["root_path"], real_path)
    result = LoaderResult()

    status_code, body, last_modified = await client.get_data(
        bucket, norm_path, expiration=None
    )

    if status_code != 200:
        result.error = LoaderResult.ERROR_NOT_FOUND
        result.extra = body
        result.successful = False
        return result

    result.successful = True
    result.buffer = body

    result.metadata.update(
        size=len(body),
        updated_at=last_modified,
    )

    return result


def get_bucket_and_path(configured_bucket: str, path: str) -> (str, str):
    bucket = configured_bucket
    real_path = path

    if not bucket:
        split_path = path.lstrip("/").split("/")
        bucket = split_path[0]
        real_path = "/".join(split_path[1:])

    return bucket, real_path


def normalize_url(prefix: str, path: str) -> str:
    """Function to normalize URLs before reaching into S3"""
    if prefix:
        return f"{prefix.rstrip('/')}/{path.lstrip('/')}"
    return path
