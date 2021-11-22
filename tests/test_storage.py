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
from tornado.testing import gen_test

from tests import BaseS3TestCase


@pytest.mark.usefixtures("test_images")
class StorageTestCase(BaseS3TestCase):
    @gen_test
    async def test_can_put_file_in_s3(self):
        """Verifies that an image can be placed in S3 using Storage and that it's there"""

        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        expected = self.test_images["default"]

        path = await storage.put(filepath, expected)

        expect(path).to_equal(
            f"https://test-bucket.s3.localhost.localstack.cloud:4566{filepath}",
        )
        status, data, _ = await storage.get_data(filepath)
        expect(status).to_equal(200)
        expect(data).to_equal(expected)

    @gen_test
    async def test_can_put_crypto_in_s3(self):
        """Verifies that security information can be placed in S3 using Storage"""

        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"

        path = await storage.put_crypto(filepath)

        expect(path).to_equal(
            f"https://test-bucket.s3.localhost.localstack.cloud:4566{filepath}.txt",
        )
        status, data, _ = await storage.get_data(filepath + ".txt")
        expect(status).to_equal(200)
        expect(data).to_equal("ACME-SEC")

    @gen_test
    async def test_can_put_detector_data_in_s3(self):
        """Verifies that detector data can be placed in S3 using Storage"""

        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"

        path = await storage.put_detector_data(
            filepath,
            {
                "some": "data",
            },
        )

        expect(path).to_equal(
            f"https://test-bucket.s3.localhost.localstack.cloud:4566{filepath}.detectors.txt",
        )
        status, data, _ = await storage.get_data(filepath + ".detectors.txt")
        expect(status).to_equal(200)
        expect(data).to_equal(b'{"some": "data"}')

    @gen_test
    async def test_can_load_file_in_s3(self):
        """Verifies that an image can be loaded from S3 using Storage"""

        storage = await self.ensure_bucket()
        filepath = f"/test/can_load_file_{uuid4()}"
        expected = self.test_images["default"]
        await storage.put(filepath, expected)

        data = await storage.get(filepath)

        expect(data).to_equal(expected)

    @gen_test
    async def test_can_handle_expired_data(self):
        """Verifies that an image won't be loaded from S3 using Storage if it is expired"""
        storage = await self.ensure_bucket()
        filepath = f"/test/can_load_file_{uuid4()}"
        expected = self.test_images["default"]
        await storage.put(filepath, expected)

        status, data, _ = await storage.get_data(filepath, expiration=0)

        expect(status).to_equal(410)
        expect(data).to_equal(b"")

    @gen_test
    async def test_can_get_crypto_from_s3(self):
        """Verifies that security information can be loaded from S3 using Storage"""
        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        await storage.upload(filepath + ".txt", b"ACME-SEC2", "application/text")

        data = await storage.get_crypto(filepath)

        expect(data).to_equal("ACME-SEC2")

    @gen_test
    async def test_can_get_detector_data_from_s3(self):
        """Verifies that detector data can be loaded from S3 using Storage"""
        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        await storage.upload(
            filepath + ".detectors.txt", b'{"some": "data"}', "application/json"
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

        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"

        exists = await storage.exists(filepath)

        expect(exists).to_be_false()

    @gen_test
    async def test_verify_file_does_exist(self):
        """Verifies that Storage can tell if a file exists in S3"""

        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        await storage.upload(filepath, self.test_images["default"], "image/jpeg")

        exists = await storage.exists(filepath)

        expect(exists).to_be_true()

    @gen_test
    async def test_can_remove(self):
        """Verifies that Storage can remove a file from S3"""

        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        await storage.upload(filepath, self.test_images["default"], "image/jpeg")
        exists = await storage.exists(filepath)
        expect(exists).to_be_true()

        await storage.remove(filepath)

        exists = await storage.exists(filepath)
        expect(exists).to_be_false()

    @gen_test
    async def test_can_remove_invalid_file(self):
        """Verifies that removing a file that does not exist does not cause Storage to fail"""

        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        exists = await storage.exists(filepath)
        expect(exists).to_be_false()

        await storage.remove(filepath)

        exists = await storage.exists(filepath)
        expect(exists).to_be_false()
