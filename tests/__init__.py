#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

import os

from thumbor.config import Config
from thumbor.context import Context, ServerParameters
from thumbor.importer import Importer
from thumbor.testing import TestCase

from thumbor_aws.s3_client import S3Client


class BaseS3TestCase(TestCase):
    test_images = {}

    @property
    def bucket_name(self):
        """Name of the bucket to put test files in"""
        return self.context.config.AWS_STORAGE_BUCKET_NAME

    @property
    def region_name(self):
        """Name of the bucket to put test files in"""
        if self.context.config.RUN_IN_COMPATIBILITY_MODE:
            return self.context.config.TC_AWS_REGION
        return self.context.config.AWS_STORAGE_REGION_NAME

    def get_config(self) -> Config:
        # Required by Bot
        os.environ["AWS_ACCESS_KEY_ID"] = "foobar"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "foobar"

        cfg = Config(SECURITY_KEY="ACME-SEC")
        cfg.LOADER = "thumbor_aws.loader"
        cfg.STORAGE = "thumbor_aws.storage"
        cfg.RESULT_STORAGE = "thumbor_aws.result_storage"

        # Storage Config
        cfg.AWS_STORAGE_REGION_NAME = "local"
        cfg.AWS_STORAGE_BUCKET_NAME = "test-bucket-st"
        cfg.AWS_STORAGE_ROOT_PATH = "/test-st"
        cfg.AWS_STORAGE_S3_ENDPOINT_URL = "https://localhost:4566"

        # Result Storage Config
        cfg.AWS_RESULT_STORAGE_REGION_NAME = "local"
        cfg.AWS_RESULT_STORAGE_BUCKET_NAME = "test-bucket-rs"
        cfg.AWS_RESULT_STORAGE_S3_ENDPOINT_URL = "https://localhost:4566"
        cfg.AWS_RESULT_STORAGE_ROOT_PATH = "/test-rs"
        cfg.STORES_CRYPTO_KEY_FOR_EACH_IMAGE = True

        # Loader Config
        cfg.AWS_LOADER_REGION_NAME = "local"
        cfg.AWS_LOADER_BUCKET_NAME = "test-bucket-st"
        cfg.AWS_LOADER_ROOT_PATH = "/test-st"
        cfg.AWS_LOADER_S3_ENDPOINT_URL = "https://localhost:4566"

        return cfg

    def get_compatibility_config(self) -> Config:
        # Required by Boto
        os.environ["AWS_ACCESS_KEY_ID"] = "foobar"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "foobar"

        cfg = Config(SECURITY_KEY="ACME-SEC")
        cfg.LOADER = "thumbor_aws.loader"
        cfg.STORAGE = "thumbor_aws.storage"
        cfg.RESULT_STORAGE = "thumbor_aws.result_storage"

        cfg.RUN_IN_COMPATIBILITY_MODE = True
        cfg.TC_AWS_REGION = "local"
        cfg.TC_AWS_MAX_RETRY = 0
        cfg.TC_AWS_ENDPOINT = "https://localhost:4566"

        # Storage Config
        cfg.TC_AWS_STORAGE_BUCKET = "test-bucket-compat"
        cfg.TC_AWS_STORAGE_ROOT_PATH = "/test-compat-st"

        # Result Storage Config
        cfg.TC_AWS_RESULT_STORAGE_BUCKET = "test-bucket-compat-rs"
        cfg.TC_AWS_RESULT_STORAGE_ROOT_PATH = "/test-compat-rs"
        cfg.STORES_CRYPTO_KEY_FOR_EACH_IMAGE = True

        # Loader Config
        cfg.TC_AWS_LOADER_BUCKET = "test-bucket-compat"
        cfg.TC_AWS_LOADER_ROOT_PATH = "/test-compat-st"

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

    async def ensure_bucket(self):
        """Ensures the test bucket is created"""
        s3client = S3Client(self.context)
        if self.context.config.RUN_IN_COMPATIBILITY_MODE is True:
            s3client.configuration["region_name"] = self.config.TC_AWS_REGION
            s3client.configuration[
                "endpoint_url"
            ] = self.config.TC_AWS_ENDPOINT

        location = {
            "LocationConstraint": self.region_name,
        }
        async with s3client.get_client() as client:
            try:
                await client.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration=location,
                )
            except client.exceptions.BucketAlreadyOwnedByYou:
                pass
