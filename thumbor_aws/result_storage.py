#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com


from datetime import datetime, timezone
from urllib.parse import unquote

from deprecated import deprecated
from thumbor.engines import BaseEngine
from thumbor.result_storages import BaseStorage, ResultStorageResult
from thumbor.utils import logger

from thumbor_aws.config import Config
from thumbor_aws.s3_client import S3Client

Config.define(
    "AWS_RESULT_STORAGE_REGION_NAME",
    "us-east-1",
    "Region where thumbor's objects are going to be stored.",
    "AWS Result Storage",
)

Config.define(
    "AWS_RESULT_STORAGE_BUCKET_NAME",
    "thumbor",
    "S3 Bucket where thumbor's objects are going to be stored.",
    "AWS Result Storage",
)

Config.define(
    "AWS_RESULT_STORAGE_S3_SECRET_ACCESS_KEY",
    None,
    "Secret access key for S3 to allow thumbor to store objects there.",
    "AWS Result Storage",
)

Config.define(
    "AWS_RESULT_STORAGE_S3_ACCESS_KEY_ID",
    None,
    "Access key ID for S3 to allow thumbor to store objects there.",
    "AWS Result Storage",
)

Config.define(
    "AWS_RESULT_STORAGE_S3_ENDPOINT_URL",
    None,
    "Endpoint URL for S3 API. Very useful for testing.",
    "AWS Result Storage",
)

Config.define(
    "AWS_RESULT_STORAGE_ROOT_PATH",
    "/rs",
    "Result Storage prefix path.",
    "AWS Result Storage",
)

Config.define(
    "AWS_RESULT_STORAGE_S3_ACL",
    None,
    "ACL to use for storing items in S3.",
    "AWS Result Storage",
)


class Storage(BaseStorage, S3Client):
    def __init__(self, context):
        BaseStorage.__init__(self, context)
        S3Client.__init__(self, context)
        if self.compatibility_mode:
            self.configuration["region_name"] = self.config.TC_AWS_REGION
            self.configuration["endpoint_url"] = self.config.TC_AWS_ENDPOINT
            self.configuration[
                "bucket_name"
            ] = self.config.TC_AWS_RESULT_STORAGE_BUCKET
            self.configuration[
                "root_path"
            ] = self.config.TC_AWS_RESULT_STORAGE_ROOT_PATH

    @property
    def region_name(self) -> str:
        return self.configuration.get(
            "region_name", self.context.config.AWS_RESULT_STORAGE_REGION_NAME
        )

    @property
    def secret_access_key(self) -> str:
        return self.configuration.get(
            "secret_access_key",
            self.context.config.AWS_RESULT_STORAGE_S3_SECRET_ACCESS_KEY,
        )

    @property
    def access_key_id(self) -> str:
        return self.configuration.get(
            "access_key_id",
            self.context.config.AWS_RESULT_STORAGE_S3_ACCESS_KEY_ID,
        )

    @property
    def endpoint_url(self) -> str:
        return self.configuration.get(
            "endpoint_url",
            self.context.config.AWS_RESULT_STORAGE_S3_ENDPOINT_URL,
        )

    @property
    def bucket_name(self) -> str:
        return self.configuration.get(
            "bucket_name",
            self.context.config.AWS_RESULT_STORAGE_BUCKET_NAME,
        )

    @property
    def file_acl(self) -> str:
        return self.configuration.get(
            "file_acl",
            self.context.config.AWS_RESULT_STORAGE_S3_ACL,
        )

    @property
    def root_path(self) -> str:
        """Defines the path prefix for all result storage images in S3"""

        return self.configuration.get(
            "root_path",
            self.context.config.AWS_RESULT_STORAGE_ROOT_PATH,
        )

    async def put(self, image_bytes: bytes) -> str:
        file_abspath = self.normalize_path(self.context.request.url)
        logger.debug("[RESULT_STORAGE] putting at %s", file_abspath)
        content_type = BaseEngine.get_mimetype(image_bytes)
        response = await self.upload(
            file_abspath,
            image_bytes,
            content_type,
            self.context.config.AWS_DEFAULT_LOCATION,
        )
        logger.info(
            "[RESULT_STORAGE] Image uploaded successfully to %s", file_abspath
        )
        return response

    @property
    def is_auto_webp(self) -> bool:
        """
        Identifies the current request if it's
        being auto converted to webp
        """
        return (
            self.context.config.AUTO_WEBP and self.context.request.accepts_webp
        )

    def normalize_path(self, path: str) -> str:
        """Returns the path used for result storage"""
        prefix = "auto_webp/" if self.is_auto_webp else ""
        fs_path = unquote(path).lstrip("/")
        return (
            f"{self.root_path.rstrip('/')}/"
            f"{prefix.lstrip('/')}"
            f"{fs_path.lstrip('/')}"
        )

    async def get(self) -> ResultStorageResult:
        path = self.context.request.url
        file_abspath = self.normalize_path(path)

        logger.debug("[RESULT_STORAGE] getting from %s", file_abspath)

        exists = await self.object_exists(file_abspath)
        if not exists:
            logger.debug(
                "[RESULT_STORAGE] image not found at %s", file_abspath
            )
            return None

        status, body, last_modified = await self.get_data(
            self.bucket_name, file_abspath
        )

        if status != 200 or self._is_expired(last_modified):
            logger.debug(
                "[RESULT_STORAGE] cached image has expired (status %s)", status
            )
            return None

        logger.info(
            "[RESULT_STORAGE] Image retrieved successfully at %s.",
            file_abspath,
        )

        return ResultStorageResult(
            buffer=body,
            metadata={
                "LastModified": last_modified.replace(tzinfo=timezone.utc),
                "ContentLength": len(body),
                "ContentType": BaseEngine.get_mimetype(body),
            },
        )

    @deprecated(version="7.0.0", reason="Use result's last_modified instead")
    async def last_updated(  # pylint: disable=invalid-overridden-method
        self,
    ) -> datetime:
        path = self.context.request.url
        file_abspath = self.normalize_path(path)
        logger.debug("[RESULT_STORAGE] getting from %s", file_abspath)

        response = await self.get_object_acl(file_abspath)
        return datetime.strptime(
            response["ResponseMetadata"]["HTTPHeaders"]["last-modified"],
            "%a, %d %b %Y %H:%M:%S %Z",
        )
