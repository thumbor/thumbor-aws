from os.path import abspath, dirname, join
from typing import Mapping

import pytest

ROOT_PATH = dirname(__file__)


@pytest.fixture(scope="class")
def test_images(request) -> Mapping[str, bytes]:
    images = [
        ("default", "image.jpg"),
    ]
    result = {}

    for key, filename in images:
        path = abspath(join(ROOT_PATH, "./fixtures", filename))
        with open(path, "rb") as image:
            result[key] = image.read()

    request.cls.test_images = result
