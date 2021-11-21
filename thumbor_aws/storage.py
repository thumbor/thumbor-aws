#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

import datetime
from json import dumps, loads
from typing import Any, Mapping, Optional

from aiobotocore.client import AioBaseClient
from aiobotocore.session import AioSession, get_session

import thumbor.storages.file_storage as file_storage
from thumbor.config import Config
from thumbor.utils import logger

Config.define(
    "AWS_STORAGE_REGION_NAME",
    "us-east-1",
    "Region where thumbor's objects are going to be stored.",
    "Storage",
)

Config.define(
    "AWS_STORAGE_BUCKET_NAME",
    "thumbor",
    "S3 Bucket where thumbor's objects are going to be stored.",
    "Storage",
)

Config.define(
    "AWS_STORAGE_S3_SECRET_ACCESS_KEY",
    None,
    "Secret access key for S3 to allow thumbor to store objects there.",
    "Storage",
)

Config.define(
    "AWS_STORAGE_S3_ACCESS_KEY_ID",
    None,
    "Access key ID for S3 to allow thumbor to store objects there.",
    "Storage",
)

Config.define(
    "AWS_STORAGE_S3_ENDPOINT_URL",
    None,
    "Endpoint URL for S3 API. Very useful for testing.",
    "Storage",
)


class Storage(file_storage.Storage):
    __session: AioSession = None
    __client: AioBaseClient = None

    @property
    def Session(self) -> AioSession:
        if self.__session is None:
            self.__session = get_session()
        return self.__session

    def get_client(self) -> AioBaseClient:
        return self.Session.create_client(
            "s3",
            region_name=self.context.config.AWS_STORAGE_REGION_NAME,
            aws_secret_access_key=self.context.config.AWS_STORAGE_S3_SECRET_ACCESS_KEY,
            aws_access_key_id=self.context.config.AWS_STORAGE_S3_ACCESS_KEY_ID,
            endpoint_url=self.context.config.AWS_STORAGE_S3_ENDPOINT_URL,
        )

    async def put(self, path: str, file_bytes: bytes) -> str:
        path = await self.upload(path, file_bytes)
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
        s3_path = await self.upload(crypto_path, key)

        logger.debug("Stored crypto at %s", crypto_path)

        return s3_path

    async def put_detector_data(self, path: str, data: Any) -> str:
        filepath = f"{path}.detectors.txt"
        details = dumps(data)
        return await self.upload(filepath, details)

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
        bucket = self.context.config.AWS_STORAGE_BUCKET_NAME
        async with self.get_client() as client:
            try:
                await client.get_object_acl(Bucket=bucket, Key=path.lstrip("/"))
                return True
            except client.exceptions.NoSuchKey:
                return False

    async def remove(self, path: str):
        raise NotImplementedError()

    async def upload(
        self,
        filepath: str,
        data: bytes,
    ) -> str:
        bucket = self.context.config.AWS_STORAGE_BUCKET_NAME
        path = filepath.lstrip("/")
        async with self.get_client() as client:
            response = None
            try:
                response = await client.put_object(
                    Bucket=bucket,
                    Key=path,
                    Body=data,
                )
            except Exception as e:
                msg = f"Unable to upload image to {path}: {e} ({type(e)})"
                logger.error(msg)
                raise RuntimeError(msg)
            status_code = self.get_status_code(response)
            if status_code != 200:
                msg = f"Unable to upload image to {path}: Status Code {status_code}"
                logger.error(msg)
                raise RuntimeError(msg)
            location = self.get_location(response)
            if location is None:
                msg = f"Unable to process response from AWS to {path}: Location Headers was not found in response"
                logger.error(msg)
                raise RuntimeError(msg)

            return f"{location.rstrip('/')}/{path}"

    async def get_data(
        self, filepath: str, expiration: int = None
    ) -> (int, bytes, Optional[datetime.datetime]):
        bucket = self.context.config.AWS_STORAGE_BUCKET_NAME
        path = filepath.lstrip("/")
        async with self.get_client() as client:
            response = await client.get_object(Bucket=bucket, Key=path)

            status_code = self.get_status_code(response)
            if status_code != 200:
                msg = f"Unable to upload image to {path}: Status Code {status_code}"
                logger.error(msg)
                return status_code, msg, None

            last_modified = response["LastModified"]
            if self.__is_expired(last_modified, expiration):
                return 410, b"", last_modified

            body = await self.get_body(response)

            return status_code, body, last_modified

    def get_status_code(self, response: Mapping[str, Any]) -> int:
        if (
            "ResponseMetadata" not in response
            or "HTTPStatusCode" not in response["ResponseMetadata"]
        ):
            return 500
        return response["ResponseMetadata"]["HTTPStatusCode"]

    def get_location(self, response: Mapping[str, Any]) -> Optional[str]:
        if (
            "ResponseMetadata" not in response
            or "HTTPHeaders" not in response["ResponseMetadata"]
            or "location" not in response["ResponseMetadata"]["HTTPHeaders"]
        ):
            return None
        return response["ResponseMetadata"]["HTTPHeaders"]["location"]

    async def get_body(self, response: Any) -> bytes:
        async with response["Body"] as stream:
            return await stream.read()

    def __is_expired(
        self, last_modified: datetime.datetime, expiration: int = None
    ) -> bool:
        if expiration is None:
            expiration = self.context.config.STORAGE_EXPIRATION_SECONDS

        if expiration is None:
            return False

        print(last_modified)
        timediff = datetime.datetime.now(datetime.timezone.utc) - last_modified
        return timediff.total_seconds() > expiration
