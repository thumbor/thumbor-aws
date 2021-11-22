#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

from json import dumps, loads
from typing import Any

from thumbor import storages
from thumbor.engines import BaseEngine
from thumbor.utils import logger
from thumbor_aws.s3_client import S3Client


class Storage(storages.BaseStorage, S3Client):
    async def put(self, path: str, file_bytes: bytes) -> str:
        content_type = BaseEngine.get_mimetype(file_bytes)
        path = await self.upload(path, file_bytes, content_type)
        return path

    async def put_crypto(self, path: str) -> str:
        if not self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
            return

        if not self.context.server.security_key:
            raise RuntimeError(
                "STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be "
                "True if no SECURITY_KEY specified"
            )

        crypto_path = f"{path}.txt"
        key = self.context.server.security_key.encode()
        s3_path = await self.upload(crypto_path, key, "application/text")

        logger.debug("Stored crypto at %s", crypto_path)

        return s3_path

    async def put_detector_data(self, path: str, data: Any) -> str:
        filepath = f"{path}.detectors.txt"
        details = dumps(data)
        return await self.upload(filepath, details, "application/json")

    async def get(self, path: str) -> bytes:
        status, body, _ = await self.get_data(path)
        if status != 200:
            raise RuntimeError(body)

        return body

    async def get_crypto(self, path: str) -> str:
        crypto_path = f"{path}.txt"
        status, body, _ = await self.get_data(crypto_path)
        if status != 200:
            raise RuntimeError(f"Failed to get crypto for {path}: {body}")

        return body.decode("utf-8")

    async def get_detector_data(self, path: str) -> Any:
        detector_path = f"{path}.detectors.txt"
        status, body, _ = await self.get_data(detector_path)
        if status != 200:
            raise RuntimeError(f"Failed to get detector data for {path}: {body}")

        return loads(body)

    async def exists(self, path: str) -> bool:
        return await self.object_exists(path)

    async def remove(self, path: str):
        exists = await self.exists(path)
        if not exists:
            return

        async with self.get_client() as client:
            response = await client.delete_object(
                Bucket=self.bucket_name, Key=path.lstrip("/")
            )
            status = self.get_status_code(response)
            if status >= 300:
                raise RuntimeError(f"Failed to remove {path}: Status {status}")
