#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

from uuid import uuid4

import pytest
from preggy import expect
from thumbor.config import Config
from tornado.testing import gen_test

from tests import BaseS3TestCase
import thumbor_aws.loader
from thumbor_aws.storage import Storage


@pytest.mark.usefixtures("test_images")
class LoaderTestCase(BaseS3TestCase):
    def setUp(self):
        super().setUp()
        thumbor_aws.loader.S3_CLIENT = None

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

        result = await thumbor_aws.loader.load(self.context, filepath)

        expect(result.successful).to_be_true()
        expect(result.buffer).to_equal(expected)
        expect(result.metadata["size"]).to_equal(len(expected))
        expect(result.metadata["updated_at"]).not_to_be_null()


@pytest.mark.usefixtures("test_images")
class LoaderCompatibilityModeTestCase(LoaderTestCase):
    def get_config(self) -> Config:
        return self.get_compatibility_config()

    @property
    def _prefix(self):
        return "/test-compat-st"

    @property
    def bucket_name(self):
        """Name of the bucket to put test files in"""
        return "test-bucket-compat"


@pytest.mark.usefixtures("test_images")
class EmptyBucketConfigLoaderTestCase(BaseS3TestCase):
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

        filepath_with_bucket = (
            f"/{self.context.config.AWS_LOADER_BUCKET_NAME}{filepath}"
        )

        self.context.config.AWS_LOADER_BUCKET_NAME = ""

        result = await load(self.context, filepath_with_bucket)

        expect(result.successful).to_be_true()
        expect(result.buffer).to_equal(expected)
        expect(result.metadata["size"]).to_equal(len(expected))
        expect(result.metadata["updated_at"]).not_to_be_null()
