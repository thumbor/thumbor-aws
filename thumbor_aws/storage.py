#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

from json import dumps, loads
from typing import Any
from urllib.parse import unquote

from thumbor import storages
from thumbor.engines import BaseEngine
from thumbor.utils import logger

from thumbor_aws.config import Config
from thumbor_aws.s3_client import S3Client
from thumbor_aws.utils import normalize_path


Config.define(
    "AWS_STORAGE_REGION_NAME",
    "us-east-1",
    "Region where thumbor's objects are going to be stored.",
    "AWS Storage",
)

Config.define(
    "AWS_STORAGE_BUCKET_NAME",
    "thumbor",
    "S3 Bucket where thumbor's objects are going to be stored.",
    "AWS Storage",
)

Config.define(
    "AWS_STORAGE_S3_SECRET_ACCESS_KEY",
    None,
    "Secret access key for S3 to allow thumbor to store objects there.",
    "AWS Storage",
)

Config.define(
    "AWS_STORAGE_S3_ACCESS_KEY_ID",
    None,
    "Access key ID for S3 to allow thumbor to store objects there.",
    "AWS Storage",
)

Config.define(
    "AWS_STORAGE_S3_ENDPOINT_URL",
    None,
    "Endpoint URL for S3 API. Very useful for testing.",
    "AWS Storage",
)

Config.define(
    "AWS_STORAGE_ROOT_PATH",
    "/st",
    "Storage prefix path.",
    "AWS Storage",
)

Config.define(
    "AWS_STORAGE_S3_ACL",
    "public-read",
    "Storage ACL for files written in bucket",
    "AWS Storage",
)

Config.define(
    "AWS_NORMALIZER",
    lambda path: unquote(path).lstrip("/"),
    "How to normalize storage paths before adding the prefix",
    "AWS Storage",
)


class Storage(storages.BaseStorage, S3Client):
    def __init__(self, context):
        S3Client.__init__(self, context)
        storages.BaseStorage.__init__(self, context)
        if self.compatibility_mode:
            self.configuration["region_name"] = self.config.TC_AWS_REGION
            self.configuration["endpoint_url"] = self.config.TC_AWS_ENDPOINT
            self.configuration[
                "bucket_name"
            ] = self.config.TC_AWS_STORAGE_BUCKET
            self.configuration[
                "root_path"
            ] = self.config.TC_AWS_STORAGE_ROOT_PATH

    @property
    def root_path(self) -> str:
        """Defines the path prefix for all storage images in S3"""
        return self.configuration.get(
            "root_path",
            self.config.AWS_STORAGE_ROOT_PATH,
        )

    async def put(self, path: str, file_bytes: bytes) -> str:
        content_type = BaseEngine.get_mimetype(file_bytes)
        normalized_path = normalize_path(self.context, self.root_path, path)
        logger.debug("[STORAGE] putting at %s", normalized_path)
        path = await self.upload(
            normalized_path,
            file_bytes,
            content_type,
            self.context.config.AWS_DEFAULT_LOCATION,
        )
        return path

    async def put_crypto(self, path: str) -> str:
        if not self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
            return

        if not self.context.server.security_key:
            raise RuntimeError(
                "STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be "
                "True if no SECURITY_KEY specified"
            )

        normalized_path = normalize_path(self.context, self.root_path, path)
        crypto_path = f"{normalized_path}.txt"
        key = self.context.server.security_key.encode()
        s3_path = await self.upload(
            crypto_path,
            key,
            "application/text",
            self.context.config.AWS_DEFAULT_LOCATION,
        )

        logger.debug("Stored crypto at %s", crypto_path)

        return s3_path

    async def put_detector_data(self, path: str, data: Any) -> str:
        normalized_path = normalize_path(self.context, self.root_path, path)
        filepath = f"{normalized_path}.detectors.txt"
        details = dumps(data)
        return await self.upload(
            filepath,
            details,
            "application/json",
            self.context.config.AWS_DEFAULT_LOCATION,
        )

    async def get(self, path: str) -> bytes:
        normalized_path = normalize_path(self.context, self.root_path, path)
        status, body, _ = await self.get_data(
            self.bucket_name, normalized_path
        )
        if status != 200:
            return None

        return body

    async def get_crypto(self, path: str) -> str:
        normalized_path = normalize_path(self.context, self.root_path, path)
        crypto_path = f"{normalized_path}.txt"
        status, body, _ = await self.get_data(self.bucket_name, crypto_path)
        if status != 200:
            return None

        return body.decode("utf-8")

    async def get_detector_data(self, path: str) -> Any:
        normalized_path = normalize_path(self.context, self.root_path, path)
        detector_path = f"{normalized_path}.detectors.txt"
        status, body, _ = await self.get_data(self.bucket_name, detector_path)
        if status != 200:
            return None

        return loads(body)

    async def exists(self, path: str) -> bool:
        normalized_path = normalize_path(self.context, self.root_path, path)
        return await self.object_exists(normalized_path)

    async def remove(self, path: str):
        exists = await self.exists(path)
        if not exists:
            return

        async with self.get_client() as client:
            normalized_path = normalize_path(self.context, self.root_path, path)
            response = await client.delete_object(
                Bucket=self.bucket_name,
                Key=normalized_path,
            )
            status = self.get_status_code(response)
            if status >= 300:
                raise RuntimeError(
                    f"Failed to remove {normalized_path}: Status {status}"
                )
