#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2021 Bernardo Heynemann heynemann@gmail.com

from distutils.core import setup

try:
    from thumbor_aws import __version__
except ImportError:
    __version__ = "0.0.0"

TESTS_REQUIREMENTS = [
    "coverage==5.*,>=5.0.3",
    "flake8==3.*,>=3.7.9",
    "isort==4.*,>=4.3.21",
    "preggy==1.*,>=1.4.4",
    "pylint==2.*,>=2.4.4",
    "pytest==6.*,>=6.2.5",
    "pytest-asyncio==0.*,>=0.10.0",
    "pytest-cov==2.*,>=2.8.1",
    "pytest-tldr==0.*,>=0.2.1",
    "pytest-xdist==1.*,>=1.31.0",
    "yanc==0.*,>=0.3.3",
    "localstack>=0.13,<1.0.0",
    "mock==3.*,>=3.0.5",
    "pyssim==0.*,>=0.4.0",
]


setup(
    name="thumbor_aws",
    version=__version__,
    description="thumbor_aws provides extensions for thumbor using AWS",
    long_description="""
thumbor_aws provides extensions for thumbor using AWS services
""",
    keywords=("imaging face detection feature thumbnail imagemagick pil opencv"),
    author="Bernardo Heynemann",
    author_email="heynemann@gmail.com",
    url="https://github.com/thumbor/thumbor_aws",
    license="MIT",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia :: Graphics :: Presentation",
    ],
    packages=["thumbor_aws"],
    package_dir={"thumbor_aws": "thumbor_aws"},
    include_package_data=True,
    package_data={"": ["*.xml"]},
    install_requires=[
        "thumbor>=7.0.0",
        "aiobotocore>=2.0.0,<3.0.0",
        "pycurl>=7.44.1,<8.0.0",
        "deprecated>=1.2.13,<2.0.0",
    ],
    extras_require={"tests": TESTS_REQUIREMENTS},
    entry_points={
        "console_scripts": [],
    },
)
