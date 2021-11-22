#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

import datetime
from typing import Any, Mapping, Optional

from aiobotocore.client import AioBaseClient
from aiobotocore.session import AioSession, get_session

from thumbor.config import Config, config
from thumbor.utils import logger

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
    "AWS_STORAGE_S3_ACL",
    None,
    "ACL to use for storing items in S3.",
    "AWS Storage",
)

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
    "AWS Storage",
)


class S3Client:
    __session: AioSession = None
    __client: AioBaseClient = None

    @property
    def region_name(self) -> str:
        return self.context.config.AWS_STORAGE_REGION_NAME

    @property
    def secret_access_key(self) -> str:
        return self.context.config.AWS_STORAGE_S3_SECRET_ACCESS_KEY

    @property
    def access_key_id(self) -> str:
        return self.context.config.AWS_STORAGE_S3_ACCESS_KEY_ID

    @property
    def endpoint_url(self) -> str:
        return self.context.config.AWS_STORAGE_S3_ENDPOINT_URL

    @property
    def bucket_name(self) -> str:
        return self.context.config.AWS_STORAGE_BUCKET_NAME

    @property
    def file_acl(self) -> str:
        return self.context.config.AWS_STORAGE_S3_ACL

    @property
    def Session(self) -> AioSession:
        if self.__session is None:
            self.__session = get_session()
        return self.__session

    def get_client(self) -> AioBaseClient:
        return self.Session.create_client(
            "s3",
            region_name=self.region_name,
            aws_secret_access_key=self.secret_access_key,
            aws_access_key_id=self.access_key_id,
            endpoint_url=self.endpoint_url,
        )

    async def upload(
        self,
        filepath: str,
        data: bytes,
        content_type,
    ) -> str:
        path = filepath.lstrip("/")
        async with self.get_client() as client:
            response = None
            try:
                settings = dict(
                    Bucket=self.bucket_name,
                    Key=path,
                    Body=data,
                    ContentType=content_type,
                )
                if self.file_acl is not None:
                    settings["ACL"] = self.file_acl

                response = await client.put_object(**settings)
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
        path = filepath.lstrip("/")
        async with self.get_client() as client:
            response = await client.get_object(Bucket=self.bucket_name, Key=path)

            status_code = self.get_status_code(response)
            if status_code != 200:
                msg = f"Unable to upload image to {path}: Status Code {status_code}"
                logger.error(msg)
                return status_code, msg, None

            last_modified = response["LastModified"]
            if self._is_expired(last_modified, expiration):
                return 410, b"", last_modified

            body = await self.get_body(response)

            return status_code, body, last_modified

    async def object_exists(self, filepath: str):
        async with self.get_client() as client:
            try:
                await client.get_object_acl(
                    Bucket=self.bucket_name, Key=filepath.lstrip("/")
                )
                return True
            except client.exceptions.NoSuchKey:
                return False

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

    def _is_expired(
        self, last_modified: datetime.datetime, expiration: int = None
    ) -> bool:
        if expiration is None:
            expiration = self.context.config.STORAGE_EXPIRATION_SECONDS

        if expiration is None:
            return False

        print(last_modified)
        timediff = datetime.datetime.now(datetime.timezone.utc) - last_modified
        return timediff.total_seconds() > expiration


def generate_config():
    config.generate_config()


if __name__ == "__main__":
    generate_config()
