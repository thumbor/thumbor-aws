#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

import datetime
from typing import Any, Dict, Mapping, Optional, Tuple

from aiobotocore.client import AioBaseClient
from aiobotocore.session import AioSession, get_session
from thumbor.config import Config
from thumbor.context import Context
from thumbor.utils import logger

_default = object()


class S3Client:
    __session: AioSession = None
    context: Context = None
    configuration: Dict[str, object] = None

    def __init__(self, context):
        self.context = context
        self.configuration = {}

    @property
    def config(self) -> Config:
        """Thumbor config from context"""
        return self.context.config

    @property
    def compatibility_mode(self) -> bool:
        """Should thumbor-aws run in compatibility mode?"""
        return self.context.config.THUMBOR_AWS_RUN_IN_COMPATIBILITY_MODE

    @property
    def region_name(self) -> str:
        """Region to save the file to"""
        return self.configuration.get(
            "region_name", self.config.AWS_STORAGE_REGION_NAME
        )

    @property
    def secret_access_key(self) -> str:
        """Secret access key to connect to AWS with"""
        return self.configuration.get(
            "secret_access_key", self.config.AWS_STORAGE_S3_SECRET_ACCESS_KEY
        )

    @property
    def access_key_id(self) -> str:
        """Access key ID to connect to AWS with"""
        return self.configuration.get(
            "access_key_id", self.config.AWS_STORAGE_S3_ACCESS_KEY_ID
        )

    @property
    def endpoint_url(self) -> str:
        """AWS Endpoint URL. Very useful for testing"""
        return self.configuration.get(
            "endpoint_url", self.config.AWS_STORAGE_S3_ENDPOINT_URL
        )

    @property
    def bucket_name(self) -> str:
        """Bucket to save the file to"""
        return self.configuration.get(
            "bucket_name", self.config.AWS_STORAGE_BUCKET_NAME
        )

    @property
    def file_acl(self) -> str:
        """ACL to save the files with"""
        return self.configuration.get(
            "file_acl", self.config.AWS_STORAGE_S3_ACL
        )

    @property
    def session(self) -> AioSession:
        """Singleton Session used for connecting with AWS"""
        if S3Client.__session is None:
            S3Client.__session = get_session()
        return S3Client.__session

    def get_client(self) -> AioBaseClient:
        """Gets a connected client to use for S3"""
        return self.session.create_client(
            "s3",
            region_name=self.region_name,
            aws_secret_access_key=self.secret_access_key,
            aws_access_key_id=self.access_key_id,
            endpoint_url=self.endpoint_url,
        )

    async def upload(
        self,
        path: str,
        data: bytes,
        content_type,
        default_location,
    ) -> str:
        """Uploads a File to S3"""

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
            except Exception as error:
                msg = f"Unable to upload image to {path}: {error} ({type(error)})"
                logger.error(msg)
                raise RuntimeError(msg)  # pylint: disable=raise-missing-from
            status_code = self.get_status_code(response)
            if status_code != 200:
                msg = f"Unable to upload image to {path}: Status Code {status_code}"
                logger.error(msg)
                raise RuntimeError(msg)

            location = self.get_location(response)
            if location is None:
                msg = (
                    f"Unable to process response from AWS to {path}: "
                    "Location Headers was not found in response"
                )
                logger.warning(msg)
                location = default_location.format(
                    bucket_name=self.bucket_name
                )

            return f"{location.rstrip('/')}/{path.lstrip('/')}"

    async def get_data(
        self, bucket: str, path: str, expiration: int = _default
    ) -> Tuple[int, bytes, bytes, Optional[datetime.datetime]]:
        """Gets an object's data from S3"""
        async with self.get_client() as client:
            try:
                response = await client.get_object(Bucket=bucket, Key=path)
            except client.exceptions.NoSuchKey:
                return 404, b"", None

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
        """Detects whether an object exists in S3"""

        async with self.get_client() as client:
            try:
                await client.get_object_acl(
                    Bucket=self.bucket_name, Key=filepath
                )
                return True
            except client.exceptions.NoSuchKey:
                return False

    async def get_object_acl(self, filepath: str):
        """Gets an object's metadata"""

        async with self.get_client() as client:
            return await client.get_object_acl(
                Bucket=self.bucket_name, Key=filepath
            )

    def get_status_code(self, response: Mapping[str, Any]) -> int:
        """Gets the status code from an AWS response object"""
        if (
            "ResponseMetadata" not in response
            or "HTTPStatusCode" not in response["ResponseMetadata"]
        ):
            return 500
        return response["ResponseMetadata"]["HTTPStatusCode"]

    def get_location(self, response: Mapping[str, Any]) -> Optional[str]:
        """Gets the location from an AWS response object"""
        if (
            "ResponseMetadata" not in response
            or "HTTPHeaders" not in response["ResponseMetadata"]
            or "location" not in response["ResponseMetadata"]["HTTPHeaders"]
        ):
            return None
        return response["ResponseMetadata"]["HTTPHeaders"]["location"]

    async def get_body(self, response: Any) -> bytes:
        """Gets the body from an AWS response object"""
        async with response["Body"] as stream:
            return await stream.read()

    def _get_bucket_and_path(self, path) -> Tuple[str, str]:
        bucket = self.bucket_name
        real_path = path
        if not self.bucket_name:
            split_path = path.lstrip("/").split("/")
            bucket = split_path[0]
            real_path = "/".join(split_path[1:])
        return (bucket, real_path)

    def _is_expired(
        self,
        last_modified: datetime.datetime,
        expiration: int = _default,
    ) -> bool:
        """Identifies whether an AWS S3 object is expired"""

        if expiration is None:
            return False

        if expiration is _default:
            expiration = self.config.STORAGE_EXPIRATION_SECONDS
        timediff = (
            datetime.datetime.now(datetime.timezone.utc).timestamp()
            - last_modified.timestamp()
        )
        return timediff >= expiration
