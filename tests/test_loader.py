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
from thumbor_aws.loader import load


@pytest.mark.usefixtures("test_images")
class LoaderTestCase(BaseS3TestCase):
    @gen_test
    async def test_can_load_file_from_s3(self):
        """
        Verifies that an image can be loaded from S3
        using Loader and that it's there
        """
        storage = await self.ensure_bucket()
        filepath = f"/test/can_put_file_{uuid4()}"
        expected = self.test_images["default"]
        await storage.put(filepath, expected)
        exists = await storage.exists(filepath)
        expect(exists).to_be_true()

        result = await load(storage.context, filepath)

        expect(result.successful).to_be_true()
        expect(result.buffer).to_equal(expected)
        expect(result.metadata["size"]).to_equal(len(expected))
        expect(result.metadata["updated_at"]).not_to_be_null()
