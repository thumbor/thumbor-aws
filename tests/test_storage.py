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
from thumbor_aws.storage import Storage
from thumbor_aws.utils import normalize_path


@pytest.mark.usefixtures("test_images")
class StorageTestCase(BaseS3TestCase):
    @property
    def _prefix(self):
        return "/test-st"

    @gen_test
    async def test_can_put_file_in_s3(self):
        """
        Verifies that an image can be placed in S3
        using Storage and that it's there
        """
        await self.ensure_bucket()
        storage = Storage(self.context)
        filepath = f"/test/can_put_file_{uuid4()}"
        expected = self.test_images["default"]

        path = await storage.put(filepath, expected)

        expect(path).to_equal(
            f"https://{self.bucket_name}.s3.localhost.localstack.cloud:4566"
            f"{self._prefix}{filepath}",
        )
        status, data, _ = await storage.get_data(
            self.bucket_name, normalize_path(storage.root_path, filepath)
        )
        expect(status).to_equal(200)
        expect(data).to_equal(expected)

    @gen_test
    async def test_can_put_crypto_in_s3(self):
        """
        Verifies that security information can
        be placed in S3 using Storage
        """
        await self.ensure_bucket()
        storage = Storage(self.context)
        filepath = f"/test/can_put_file_{uuid4()}"

        path = await storage.put_crypto(filepath)

        expect(path).to_equal(
            f"https://{self.bucket_name}.s3.localhost.localstack.cloud:4566"
            f"{self._prefix}{filepath}.txt",
        )
        status, data, _ = await storage.get_data(
            self.bucket_name,
            normalize_path(storage.root_path, filepath + ".txt"),
        )
        expect(status).to_equal(200)
        expect(data).to_equal("ACME-SEC")

    @gen_test
    async def test_can_put_detector_data_in_s3(self):
        """Verifies that detector data can be placed in S3 using Storage"""
        await self.ensure_bucket()
        storage = Storage(self.context)
        filepath = f"/test/can_put_file_{uuid4()}"

        path = await storage.put_detector_data(
            filepath,
            {
                "some": "data",
            },
        )

        expect(path).to_equal(
            f"https://{self.bucket_name}.s3.localhost.localstack.cloud:4566"
            f"{self._prefix}{filepath}.detectors.txt",
        )
        status, data, _ = await storage.get_data(
            self.bucket_name,
            normalize_path(storage.root_path, filepath + ".detectors.txt"),
        )
        expect(status).to_equal(200)
        expect(data).to_equal(b'{"some": "data"}')

    @gen_test
    async def test_can_load_file_in_s3(self):
        """Verifies that an image can be loaded from S3 using Storage"""
        await self.ensure_bucket()
        storage = Storage(self.context)
        filepath = f"/test/can_load_file_{uuid4()}"
        expected = self.test_images["default"]
        await storage.put(filepath, expected)

        data = await storage.get(filepath)

        expect(data).to_equal(expected)

    @gen_test
    async def test_can_handle_expired_data(self):
        """
        Verifies that an image won't be loaded from S3
        using Storage if it is expired
        """
        await self.ensure_bucket()
        storage = Storage(self.context)
        filepath = f"/test/can_load_file_{uuid4()}"
        expected = self.test_images["default"]
        await storage.put(filepath, expected)

        status, data, _ = await storage.get_data(
            self.bucket_name,
            normalize_path(storage.root_path, filepath),
            expiration=0,
        )

        expect(status).to_equal(410)
        expect(data).to_equal(b"")

    @gen_test
    async def test_can_get_crypto_from_s3(self):
        """
        Verifies that security information can be
        loaded from S3 using Storage
        """
        await self.ensure_bucket()
        storage = Storage(self.context)
        filepath = f"/test/can_put_file_{uuid4()}"

        await storage.upload(
            normalize_path(storage.root_path, filepath + ".txt"),
            b"ACME-SEC2",
            "application/text",
            "http://my-site.com",
            false
        )

        data = await storage.get_crypto(filepath)

        expect(data).to_equal("ACME-SEC2")

    @gen_test
    async def test_can_get_detector_data_from_s3(self):
        """Verifies that detector data can be loaded from S3 using Storage"""
        await self.ensure_bucket()
        storage = Storage(self.context)
        filepath = f"/test/can_put_file_{uuid4()}"
        await storage.upload(
            normalize_path(storage.root_path, filepath + ".detectors.txt"),
            b'{"some": "data"}',
            "application/text",
            "",
            false
        )

        data = await storage.get_detector_data(filepath)

        expect(data).to_be_like(
            {
                "some": "data",
            }
        )

    @gen_test
    async def test_verify_file_does_not_exist(self):
        """Verifies that Storage can tell if a file does not exist in S3"""
        await self.ensure_bucket()
        storage = Storage(self.context)
        filepath = f"/test/can_put_file_{uuid4()}"

        exists = await storage.exists(filepath)

        expect(exists).to_be_false()

    @gen_test
    async def test_verify_file_does_exist(self):
        """Verifies that Storage can tell if a file exists in S3"""
        await self.ensure_bucket()
        storage = Storage(self.context)
        filepath = f"/test/can_put_file_{uuid4()}"
        await storage.put(filepath, self.test_images["default"])

        exists = await storage.exists(filepath)

        expect(exists).to_be_true()

    @gen_test
    async def test_can_remove(self):
        """Verifies that Storage can remove a file from S3"""
        await self.ensure_bucket()
        storage = Storage(self.context)
        filepath = f"/test/can_put_file_{uuid4()}"
        await storage.put(filepath, self.test_images["default"])
        exists = await storage.exists(filepath)
        expect(exists).to_be_true()

        await storage.remove(filepath)

        exists = await storage.exists(filepath)
        expect(exists).to_be_false()

    @gen_test
    async def test_can_remove_invalid_file(self):
        """
        Verifies that removing a file that does not exist
        does not cause Storage to fail
        """
        await self.ensure_bucket()
        storage = Storage(self.context)
        filepath = f"/test/can_put_file_{uuid4()}"
        exists = await storage.exists(filepath)
        expect(exists).to_be_false()

        await storage.remove(filepath)

        exists = await storage.exists(filepath)
        expect(exists).to_be_false()


@pytest.mark.usefixtures("test_images")
class StorageCompatibilityModeTestCase(StorageTestCase):
    def get_config(self) -> Config:
        return self.get_compatibility_config()

    @property
    def _prefix(self):
        return "/test-compat-st"

    @property
    def bucket_name(self):
        """Name of the bucket to put test files in"""
        return "test-bucket-compat"
