#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com


from datetime import timezone
from urllib.parse import unquote

from thumbor.engines import BaseEngine
from thumbor.result_storages import BaseStorage, ResultStorageResult
from thumbor.utils import logger
from thumbor_aws.s3_client import S3Client


class Storage(BaseStorage, S3Client):
    @property
    def region_name(self) -> str:
        return self.context.config.AWS_RESULT_STORAGE_REGION_NAME

    @property
    def secret_access_key(self) -> str:
        return self.context.config.AWS_RESULT_STORAGE_S3_SECRET_ACCESS_KEY

    @property
    def access_key_id(self) -> str:
        return self.context.config.AWS_RESULT_STORAGE_S3_ACCESS_KEY_ID

    @property
    def endpoint_url(self) -> str:
        return self.context.config.AWS_RESULT_STORAGE_S3_ENDPOINT_URL

    @property
    def bucket_name(self) -> str:
        return self.context.config.AWS_RESULT_STORAGE_BUCKET_NAME

    @property
    def file_acl(self) -> str:
        return self.context.config.AWS_RESULT_STORAGE_S3_ACL

    @property
    def root_path(self) -> str:
        return self.context.config.AWS_RESULT_STORAGE_ROOT_PATH.rstrip("/")

    async def put(self, image_bytes: bytes) -> str:
        file_abspath = self.normalize_path(self.context.request.url)
        logger.debug(f"[RESULT_STORAGE] putting at {file_abspath}")
        content_type = BaseEngine.get_mimetype(image_bytes)
        response = await self.upload(file_abspath, image_bytes, content_type)
        logger.info(f"[RESULT_STORAGE] Image uploaded successfully to {file_abspath}")
        return response

    @property
    def is_auto_webp(self) -> bool:
        return self.context.config.AUTO_WEBP and self.context.request.accepts_webp

    def normalize_path(self, path: str) -> str:
        prefix = "auto_webp" if self.is_auto_webp else "default"
        fs_path = unquote(path).lstrip("/")
        return f"{self.root_path}/{prefix}/{fs_path}"

    async def get(self) -> ResultStorageResult:
        path = self.context.request.url
        file_abspath = self.normalize_path(path)

        logger.debug("[RESULT_STORAGE] getting from %s", file_abspath)

        exists = await self.object_exists(file_abspath)
        if not exists:
            logger.debug("[RESULT_STORAGE] image not found at %s", file_abspath)
            return None

        status, body, last_modified = await self.get_data(file_abspath)

        if status != 200 or self._is_expired(last_modified):
            logger.debug(f"[RESULT_STORAGE] cached image has expired (status {status})")
            return None

        logger.info(f"[RESULT_STORAGE] Image retrieved successfully at {file_abspath}.")

        return ResultStorageResult(
            buffer=body,
            metadata={
                "LastModified": last_modified.replace(tzinfo=timezone.utc),
                "ContentLength": len(body),
                "ContentType": BaseEngine.get_mimetype(body),
            },
        )
