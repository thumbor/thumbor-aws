#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor aws extensions
# https://github.com/thumbor/thumbor-aws

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

import asyncio
from os import listdir
from os.path import abspath, dirname, isfile, join

from aiobotocore.session import get_session
from thumbor.utils import logger

ROOT_PATH = dirname(__file__)


async def upload():
    """Uploads file to S3"""
    images_path = abspath(join(ROOT_PATH, "tests", "fixtures"))
    all_images = [
        f for f in listdir(images_path) if isfile(join(images_path, f))
    ]

    session = get_session()
    async with session.create_client(
        "s3",
        region_name="us-east-1",
        endpoint_url="https://localhost:4566",
    ) as client:

        # Ensure Bucket is there
        try:
            location = {"LocationConstraint": "us-east-1"}
            await client.create_bucket(
                Bucket="fixtures",
                CreateBucketConfiguration=location,
            )
        except client.exceptions.BucketAlreadyOwnedByYou:
            pass

        # Then upload all images
        for image_path in all_images:
            with open(join(images_path, image_path), "rb") as image:
                content = image.read()
                response = None
                try:
                    response = await client.put_object(
                        Bucket="fixtures",
                        Key=image_path,
                        Body=content,
                        ContentType="image/jpeg",
                        ACL="public-read",
                    )
                except Exception as err:
                    msg = (
                        "Unable to upload image to "
                        f"{image_path}: {err} ({type(err)})"
                    )
                    logger.error(msg)
                    raise RuntimeError(msg) from err
                status_code = response["ResponseMetadata"]["HTTPStatusCode"]
                if status_code != 200:
                    msg = (
                        "Unable to upload image to "
                        f"{image_path}: Status Code {status_code}"
                    )
                    logger.error(msg)
                    raise RuntimeError(msg)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(upload())
