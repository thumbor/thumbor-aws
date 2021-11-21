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
    @property
    def bucket_name(self):
        return self.context.config.AWS_STORAGE_BUCKET_NAME

    def get_context(self):
        cfg = Config(SECURITY_KEY="ACME-SEC")
        cfg.STORAGE = "thumbor_aws.storage"
        cfg.AWS_STORAGE_REGION_NAME = "local"
        cfg.AWS_STORAGE_BUCKET_NAME = "test-bucket"
        cfg.AWS_STORAGE_S3_ENDPOINT_URL = "https://localhost:4566"

        importer = Importer(cfg)
        importer.import_modules()
        server = ServerParameters(8889, "localhost", "thumbor.conf", None, "info", None)
        server.security_key = "ACME-SEC"
        return Context(server, cfg, importer)

    async def ensure_bucket(self, cls=Storage):
        storage = cls(self.context)
        location = {"LocationConstraint": self.context.config.AWS_STORAGE_REGION_NAME}
        async with storage.get_client() as client:
            try:
                await client.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration=location,
                )
            except client.exceptions.BucketAlreadyOwnedByYou:
                pass
        return storage
