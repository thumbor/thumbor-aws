#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

from unittest.mock import Mock
from uuid import uuid4

import pytest
from preggy import expect
from thumbor.config import Config
from tornado.testing import gen_test

from tests import BaseS3TestCase
from thumbor_aws.result_storage import Storage as ResultStorage


@pytest.mark.usefixtures("test_images")
class ResultStorageTestCase(BaseS3TestCase):
    @property
    def bucket_name(self):
        return self.context.config.AWS_RESULT_STORAGE_BUCKET_NAME

    @property
    def _prefix(self):
        return "/test-rs"

    @property
    def region_name(self):
        """Name of the bucket to put test files in"""
        if self.context.config.THUMBOR_AWS_RUN_IN_COMPATIBILITY_MODE:
            return self.context.config.TC_AWS_REGION
        return self.context.config.AWS_RESULT_STORAGE_REGION_NAME

    @gen_test
    async def test_can_put_file_in_s3(self):
        """
        Verifies that submitting an image to S3 through
        Result Storage works and the image is there
        """
        await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        self.context.request = Mock(url=filepath)
        storage = ResultStorage(self.context)
        expected = self.test_images["default"]

        path = await storage.put(expected)

        expect(path).to_equal(
            f"https://{self.bucket_name}.s3.localhost.localstack.cloud:4566"
            f"{self._prefix}/default{filepath}",
        )
        status, data, _ = await storage.get_data(
            f"{self._prefix}/default{filepath}"
        )
        expect(status).to_equal(200)
        expect(data).to_equal(expected)

    @gen_test
    async def test_can_get_result_in_s3(self):
        """
        Verifies that an image can be retrieved
        from S3 through Result Storage
        """
        await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        self.context.request = Mock(url=filepath)
        storage = ResultStorage(self.context)
        expected = self.test_images["default"]
        await storage.put(expected)

        data = await storage.get()

        expect(data).not_to_be_null()
        expect(data.buffer).to_equal(expected)
        expect(data.metadata).to_include("LastModified")
        expect(data.metadata["ContentLength"]).to_equal(5319)
        expect(data.metadata["ContentType"]).to_equal("image/jpeg")

    @gen_test
    async def test_can_get_result_in_s3_for_invalid_file(self):
        """
        Verifies that if an image does not exist,
        Result Storage returns None
        """
        await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        self.context.request = Mock(url=filepath)
        storage = ResultStorage(self.context)

        data = await storage.get()

        expect(data).to_be_null()

    @gen_test
    async def test_can_check_deprecated_last_updated_method(self):
        """
        Verifies that Result Storage deprecated
        last_updated method works
        """
        await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        self.context.request = Mock(url=filepath)
        storage = ResultStorage(self.context)
        expected = self.test_images["default"]
        await storage.put(expected)

        last_updated = await storage.last_updated()

        expect(last_updated).not_to_be_null()


@pytest.mark.usefixtures("test_images")
class ResultStorageCompatibilityTestCase(ResultStorageTestCase):
    def get_config(self) -> Config:
        return self.get_compatibility_config()

    @property
    def _prefix(self):
        return "/test-compat-rs"

    @property
    def bucket_name(self):
        """Name of the bucket to put test files in"""
        return "test-bucket-compat-rs"
