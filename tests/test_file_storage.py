#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

from preggy import expect
from tornado.testing import gen_test

from thumbor.config import Config
from thumbor.context import Context, ServerParameters
from thumbor.importer import Importer
from thumbor.testing import TestCase
from thumbor_aws.storage import Storage


class FileStorageTestCase(TestCase):
    def get_context(self):
        cfg = Config(SECURITY_KEY="ACME-SEC")
        cfg.STORAGE = "thumbor_aws.storage"
        cfg.S3_STORAGE_BUCKET_NAME = "test-bucket"

        importer = Importer(cfg)
        importer.import_modules()
        server = ServerParameters(8889, "localhost", "thumbor.conf", None, "info", None)
        server.security_key = "ACME-SEC"
        return Context(server, cfg, importer)

    @gen_test
    async def test_can_load_put_file_in_s3(self):
        storage = Storage(self.context)
        await storage.put("test data")

        #  expect(exists(self.config.FILE_STORAGE_ROOT_PATH)).to_be_true()
