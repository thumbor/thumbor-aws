#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com


import pytest
from preggy import expect
from tornado.testing import gen_test

from tests import BaseS3TestCase

import thumbor_aws.s3_client


@pytest.mark.usefixtures("test_images")
class S3ClientTestCase(BaseS3TestCase):
    @gen_test
    async def test_should_reuse_the_same_client(self):
        """
        Verifies that the S3 client module will
        reuse the same AioBoto client.
        """
        s3client = await thumbor_aws.s3_client.S3Client(
            self.context
        ).get_client()
        s3client2 = await thumbor_aws.s3_client.S3Client(
            self.context
        ).get_client()
        expect(s3client).to_equal(s3client2)
