#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

from uuid import uuid4

import pytest
from mock import Mock
from preggy import expect
from tornado.testing import gen_test

from tests import BaseS3TestCase
from thumbor.config import Config
from thumbor.context import Context, ServerParameters
from thumbor.importer import Importer
from thumbor_aws.result_storage import Storage


@pytest.mark.usefixtures("test_images")
class ResultStorageTestCase(BaseS3TestCase):
    @property
    def bucket_name(self):
        return self.context.config.AWS_RESULT_STORAGE_BUCKET_NAME

    def get_context(self):
        cfg = Config(SECURITY_KEY="ACME-SEC")
        cfg.RESULT_STORAGE = "thumbor_aws.result_storage"
        cfg.AWS_RESULT_STORAGE_REGION_NAME = "local"
        cfg.AWS_RESULT_STORAGE_BUCKET_NAME = "test-bucket"
        cfg.AWS_RESULT_STORAGE_S3_ENDPOINT_URL = "https://localhost:4566"
        cfg.AWS_RESULT_STORAGE_ROOT_PATH = "/test-rs"
        cfg.STORES_CRYPTO_KEY_FOR_EACH_IMAGE = True

        importer = Importer(cfg)
        importer.import_modules()
        server = ServerParameters(8889, "localhost", "thumbor.conf", None, "info", None)
        server.security_key = "ACME-SEC"
        return Context(server, cfg, importer)

    @gen_test
    async def test_can_put_file_in_s3(self):
        (
            """Verifies that submitting an image to S3 through"""
            """Result Storage works and the image is there"""
        )

        filepath = f"/test/can_put_file_{uuid4()}"
        self.context.request = Mock(url=filepath)
        storage = await self.ensure_bucket(cls=Storage)
        expected = self.test_images["default"]

        path = await storage.put(expected)

        expect(path).to_equal(
            f"https://test-bucket.s3.localhost.localstack.cloud:4566/test-rs/default{filepath}",
        )
        status, data, _ = await storage.get_data(f"/test-rs/default{filepath}")
        expect(status).to_equal(200)
        expect(data).to_equal(expected)

    @gen_test
    async def test_can_get_result_in_s3(self):
        """Verifies that an image can be retrieved from S3 through Result Storage"""
        filepath = f"/test/can_put_file_{uuid4()}"
        self.context.request = Mock(url=filepath)
        storage = await self.ensure_bucket(cls=Storage)
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
        """Verifies that if an image does not exist, Result Storage returns None"""
        filepath = f"/test/can_put_file_{uuid4()}"
        self.context.request = Mock(url=filepath)
        storage = await self.ensure_bucket(cls=Storage)

        data = await storage.get()

        expect(data).to_be_null()

    @gen_test
    async def test_can_check_deprecated_last_updated_method(self):
        """Verifies that Result Storage deprecated last_updated method works"""

        filepath = f"/test/can_put_file_{uuid4()}"
        self.context.request = Mock(url=filepath)
        storage = await self.ensure_bucket(cls=Storage)
        expected = self.test_images["default"]
        await storage.put(expected)

        last_updated = await storage.last_updated()

        expect(last_updated).not_to_be_null()
