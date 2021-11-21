#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

from uuid import uuid4

from preggy import expect
from tornado.testing import gen_test

from tests import BaseS3TestCase
from thumbor.config import Config
from thumbor.context import Context, ServerParameters
from thumbor.importer import Importer


class FileStorageTestCase(BaseS3TestCase):
    def get_context(self):
        cfg = Config(SECURITY_KEY="ACME-SEC")
        cfg.STORAGE = "thumbor_aws.storage"
        cfg.AWS_STORAGE_REGION_NAME = "local"
        cfg.AWS_STORAGE_BUCKET_NAME = "test-bucket"
        cfg.AWS_STORAGE_S3_ENDPOINT_URL = "https://localhost:4566"
        cfg.STORES_CRYPTO_KEY_FOR_EACH_IMAGE = True

        importer = Importer(cfg)
        importer.import_modules()
        server = ServerParameters(8889, "localhost", "thumbor.conf", None, "info", None)
        server.security_key = "ACME-SEC"
        return Context(server, cfg, importer)

    @gen_test
    async def test_can_put_file_in_s3(self):
        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        expected = b"test data"

        path = await storage.put(filepath, expected)

        expect(path).to_equal(
            f"https://test-bucket.s3.localhost.localstack.cloud:4566{filepath}",
        )
        status, data, _ = await storage.get_data(filepath)
        expect(status).to_equal(200)
        expect(data).to_equal(expected)

    @gen_test
    async def test_can_put_crypto_in_s3(self):
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
        storage = await self.ensure_bucket()
        filepath = f"/test/can_load_file_{uuid4()}"
        expected = b"test data"
        await storage.put(filepath, expected)

        data = await storage.get(filepath)

        expect(data).to_equal(expected)

    @gen_test
    async def test_can_handle_expired_data(self):
        storage = await self.ensure_bucket()
        filepath = f"/test/can_load_file_{uuid4()}"
        expected = b"test data"
        await storage.put(filepath, expected)

        status, data, _ = await storage.get_data(filepath, expiration=0)

        expect(status).to_equal(410)
        expect(data).to_equal(b"")

    @gen_test
    async def test_can_get_crypto_from_s3(self):
        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        await storage.upload(filepath + ".txt", b"ACME-SEC2")

        data = await storage.get_crypto(filepath)

        expect(data).to_equal("ACME-SEC2")

    @gen_test
    async def test_can_get_detector_data_from_s3(self):
        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        await storage.upload(filepath + ".detectors.txt", b'{"some": "data"}')

        data = await storage.get_detector_data(filepath)

        expect(data).to_be_like(
            {
                "some": "data",
            }
        )

    @gen_test
    async def test_verify_file_does_not_exist(self):
        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"

        exists = await storage.exists(filepath)

        expect(exists).to_be_false()

    @gen_test
    async def test_verify_file_does_exists(self):
        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        await storage.upload(filepath, b'{"some": "data"}')

        exists = await storage.exists(filepath)

        expect(exists).to_be_true()

    @gen_test
    async def test_can_remove(self):
        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        await storage.upload(filepath, b'{"some": "data"}')
        exists = await storage.exists(filepath)
        expect(exists).to_be_true()

        await storage.remove(filepath)

        exists = await storage.exists(filepath)
        expect(exists).to_be_false()

    @gen_test
    async def test_can_remove_invalid_file(self):
        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        exists = await storage.exists(filepath)
        expect(exists).to_be_false()

        await storage.remove(filepath)

        exists = await storage.exists(filepath)
        expect(exists).to_be_false()
