#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

from uuid import uuid4

from unittest.mock import patch
import pytest
from preggy import expect
from thumbor.config import Config
from tornado.testing import gen_test
from tests import BaseS3TestCase
import thumbor_aws.loader
from thumbor_aws.storage import Storage
import asyncio



@pytest.mark.usefixtures("test_images")
class LoaderTestCase(BaseS3TestCase):
    @property
    def bucket_name(self):
        """Name of the bucket to put test files in"""
        return self.context.config.AWS_LOADER_BUCKET_NAME

    @gen_test
    async def test_can_load_file_from_s3(self):
        """
        Verifies that an image can be loaded from S3
        using Loader and that it's there
        """
        await self.ensure_bucket()
        storage = Storage(self.context)
        filepath = f"/test/can_put_file_{uuid4()}"
        expected = self.test_images["default"]
        await storage.put(filepath, expected)
        exists = await storage.exists(filepath)
        expect(exists).to_be_true()

        # ensures we are testing if the Thumbor HTTP Loader
        # config key was set to True and the scheme was not http
        self.context.config.AWS_ENABLE_HTTP_LOADER = True
        result = await thumbor_aws.loader.load(self.context, filepath)

        expect(result.successful).to_be_true()
        expect(result.buffer).to_equal(expected)
        expect(result.metadata["size"]).to_equal(len(expected))
        expect(result.metadata["updated_at"]).not_to_be_null()

    @gen_test
    async def test_result_false_when_file_not_in_s3(self):
        """
        Verifies that result is false when image not present in S3
        """
        await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"

        result = await thumbor_aws.loader.load(self.context, filepath)

        expect(result.successful).to_be_false()

    @pytest.fixture()
    def mock_loader(mocker):
        future = asyncio.Future()
        mocker.patch('thumbor.loaders.http_loader.load', return_value=future)
        return future
        
    # @patch('thumbor.loaders.http_loader.load')
    @gen_test
    @pytest.mark.asyncio
    async def test_should_use_http_loader(self, mock_loader):
        conf = Config(AWS_ENABLE_HTTP_LOADER=True)
        self.context.config = conf
        mock_loader.set_result(True)
        await thumbor_aws.loader.load(self.context, 'http://foo.bar')
        self.assertTrue(mock_loader.called)


@pytest.mark.usefixtures("test_images")
class LoaderCompatibilityModeTestCase(LoaderTestCase):
    def get_config(self) -> Config:
        return self.get_compatibility_config()

    @property
    def bucket_name(self):
        """Name of the bucket to put test files in"""
        return "test-bucket-compat"


@pytest.mark.usefixtures("test_images")
class EmptyBucketConfigLoaderTestCase(BaseS3TestCase):
    def get_config(self) -> Config:
        cfg = super().get_config()
        cfg.AWS_LOADER_BUCKET_NAME = ""
        return cfg

    @gen_test
    async def test_can_load_file_from_s3(self):
        """
        Verifies that an image can be loaded from S3
        using Loader and that it's there
        """
        await self.ensure_bucket()
        storage = Storage(self.context)
        filepath = f"/test/can_put_file_{uuid4()}"
        expected = self.test_images["default"]
        await storage.put(filepath, expected)
        exists = await storage.exists(filepath)
        expect(exists).to_be_true()

        filepath_with_bucket = (
            f"/{self.context.config.AWS_STORAGE_BUCKET_NAME}{filepath}"
        )

        result = await thumbor_aws.loader.load(
            self.context, filepath_with_bucket
        )

        expect(result.successful).to_be_true()
        expect(result.buffer).to_equal(expected)
        expect(result.metadata["size"]).to_equal(len(expected))
        expect(result.metadata["updated_at"]).not_to_be_null()


@pytest.mark.usefixtures("test_images")
class LoaderNoPrefixTestCase(LoaderTestCase):
    def get_config(self) -> Config:
        cfg = super().get_config()
        cfg.AWS_LOADER_BUCKET_NAME = "test-bucket-loader-no-prefix"
        cfg.AWS_STORAGE_BUCKET_NAME = "test-bucket-loader-no-prefix"
        cfg.AWS_LOADER_ROOT_PATH = ""
        cfg.AWS_STORAGE_ROOT_PATH = ""
        return cfg
