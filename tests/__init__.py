#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

from thumbor.config import Config
from thumbor.context import Context, ServerParameters
from thumbor.importer import Importer
from thumbor.testing import TestCase

from thumbor_aws.storage import Storage


class BaseS3TestCase(TestCase):
    test_images = {}

    @property
    def compatibility_mode(self):
        """Whether to run in compatibility mode or not"""
        return False

    @property
    def bucket_name(self):
        """Name of the bucket to put test files in"""
        return self.context.config.AWS_STORAGE_BUCKET_NAME

    @property
    def region_name(self):
        """Name of the bucket to put test files in"""
        return self.context.config.AWS_STORAGE_REGION_NAME

    def get_config(self) -> Config:
        cfg = Config(SECURITY_KEY="ACME-SEC")
        cfg.LOADER = "thumbor_aws.loader"
        cfg.STORAGE = "thumbor_aws.storage"
        cfg.RESULT_STORAGE = "thumbor_aws.result_storage"

        # Storage Config
        cfg.AWS_STORAGE_REGION_NAME = "local"
        cfg.AWS_STORAGE_BUCKET_NAME = "test-bucket"
        cfg.AWS_STORAGE_S3_ENDPOINT_URL = "https://localhost:4566"

        # Result Storage Config
        cfg.AWS_RESULT_STORAGE_REGION_NAME = "local"
        cfg.AWS_RESULT_STORAGE_BUCKET_NAME = "test-bucket"
        cfg.AWS_RESULT_STORAGE_S3_ENDPOINT_URL = "https://localhost:4566"
        cfg.AWS_RESULT_STORAGE_ROOT_PATH = "/test-rs"
        cfg.STORES_CRYPTO_KEY_FOR_EACH_IMAGE = True

        # Loader Config
        cfg.AWS_LOADER_REGION_NAME = "local"
        cfg.AWS_LOADER_BUCKET_NAME = "test-bucket"
        cfg.AWS_LOADER_S3_ENDPOINT_URL = "https://localhost:4566"

        return cfg

    def get_context(self) -> Context:
        cfg = self.get_config()
        importer = Importer(cfg)
        importer.import_modules()
        server = ServerParameters(
            8889, "localhost", "thumbor.conf", None, "info", None
        )
        server.security_key = "ACME-SEC"
        return Context(server, cfg, importer)

    async def ensure_bucket(self, cls=Storage):
        """Ensures the test bucket is created"""
        storage = cls(self.context)
        location = {
            "LocationConstraint": self.region_name,
        }
        async with storage.get_client() as client:
            try:
                await client.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration=location,
                )
            except client.exceptions.BucketAlreadyOwnedByYou:
                pass
        return storage
