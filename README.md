<p align="center">
<img src="https://raw.github.com/thumbor/thumbor/master/logo-thumbor.png" />
</p>

<h3 align="center">thumbor-aws</h3>

<p align="center">
This is a project to provide modern thumbor>7.0.0 AWS Extensions.
</p>

<p align="center">
  <img src='https://github.com/thumbor/thumbor-aws/workflows/build/badge.svg' />
  <a href='https://coveralls.io/github/thumbor/thumbor-aws?branch=main'><img src='https://coveralls.io/repos/github/thumbor/thumbor-aws/badge.svg?branch=main' alt='Coverage Status' /></a>

  <a href='https://codeclimate.com/github/thumbor/thumbor-aws' target='_blank'>
    <img src='https://codeclimate.com/github/thumbor/thumbor-aws/badges/gpa.svg'/>
  </a>
</p>
<p align="center">
  <a href='https://github.com/thumbor/thumbor-aws/pulls' target='_blank'>
    <img src='https://img.shields.io/github/issues-pr-raw/thumbor/thumbor-aws.svg'/>
  </a>
  <a href='https://github.com/thumbor/thumbor-aws/issues' target='_blank'>
    <img src='https://img.shields.io/github/issues-raw/thumbor/thumbor-aws.svg'/>
  </a>
  <a href='https://pypi.python.org/pypi/thumbor-aws' target='_blank'>
    <img src='https://img.shields.io/pypi/v/thumbor-aws.svg'/>
  </a>
  <a href='https://pypi.python.org/pypi/thumbor-aws' target='_blank'>
    <img src='https://img.shields.io/pypi/dm/thumbor-aws.svg'/>
  </a>
</p>

## ⚙️ Installation

```bash
pip install thumbor-aws
```
## 🎯 Features

- Asynchronous non-blocking AWS S3 support
- Conforms with thumbor 7 new storage and results storage specs
- Python 3 compliant
- S3 Image Loader - Load source images from S3
- S3 Storage - Retrieve and store source images, detector data and security keys
- S3 Result Storage - Retrieve and store resulting images
- Compatibility mode for users of tc_aws: currently supported loader, storage and result storage

## Usage

### Configuring thumbor

Configure your `thumbor.conf` file to point to `thumbor_aws`:

```
## The loader thumbor should use to find source images.
## This must be the full name of a python module (python must be able to import it)
LOADER = "thumbor.loaders.http_loader"

## The file storage thumbor should use to store original images.
## This must be the full name of a python module (python must be able to import it)
STORAGE = 'thumbor_aws.storage'

## The result storage thumbor should use to store generated images.
## This must be the full name of a python module (python must be able to import it)
RESULT_STORAGE = 'thumbor_aws.result_storage'
```

You should use only the extensions required by your use case.
There's no dependency between them.

### Configuration

thumbor-aws allows you to configure each extension independently:

#### General

Some S3 providers fail to return a valid location header when uploading a new object. For that scenario, `thumbor-aws` allows users to set the location template to be used.

```
## Default location to use if S3 does not return location header.
## Can use {bucket_name} var.
## Defaults to: 'https://{bucket_name}.s3.amazonaws.com'
AWS_DEFAULT_LOCATION = "https://{bucket_name}.s3.amazonaws.com"
```

#### Loader

thumbor-aws loader offer several configuration options:

```python
################################## AWS Loader ##################################

## Region where thumbor's objects are going to be loaded from.
## Defaults to: 'us-east-1'
#AWS_LOADER_REGION_NAME = 'us-east-1'

## S3 Bucket where thumbor's objects are loaded from.
## Defaults to: 'thumbor'
#AWS_LOADER_BUCKET_NAME = 'thumbor'

## Secret access key for S3 Loader.
## Defaults to: None
#AWS_LOADER_S3_SECRET_ACCESS_KEY = None

## Access key ID for S3 Loader.
## Defaults to: None
#AWS_LOADER_S3_ACCESS_KEY_ID = None

## Endpoint URL for S3 API. Very useful for testing.
## Defaults to: None
#AWS_LOADER_S3_ENDPOINT_URL = None

## Loader prefix path.
## Defaults to: '/st'
#AWS_LOADER_ROOT_PATH = '/st'

################################################################################
```

#### Storage

Below you can see the result of running thumbor's config generation after importing thumbor-aws:

```
################################# AWS Storage ##################################

## Region where thumbor's objects are going to be stored.
## Defaults to: 'us-east-1'
#AWS_STORAGE_REGION_NAME = 'us-east-1'

## S3 Bucket where thumbor's objects are going to be stored.
## Defaults to: 'thumbor'
#AWS_STORAGE_BUCKET_NAME = 'thumbor'

## Secret access key for S3 to allow thumbor to store objects there.
## Defaults to: None
#AWS_STORAGE_S3_SECRET_ACCESS_KEY = None

## Access key ID for S3 to allow thumbor to store objects there.
## Defaults to: None
#AWS_STORAGE_S3_ACCESS_KEY_ID = None

## Endpoint URL for S3 API. Very useful for testing.
## Defaults to: None
#AWS_STORAGE_S3_ENDPOINT_URL = None

## Storage prefix path.
## Defaults to: '/st'
#AWS_STORAGE_ROOT_PATH = '/st'

## Storage ACL for files written in bucket
## Defaults to: 'public-read'
#AWS_STORAGE_S3_ACL = 'public-read'

## Default location to use if S3 does not return location header. Can use
## {bucket_name} var.
## Defaults to: 'https://{bucket_name}.s3.amazonaws.com'
#AWS_DEFAULT_LOCATION = 'https://{bucket_name}.s3.amazonaws.com'

################################################################################

```

#### Result Storage

Below you can see the result of running thumbor's config generation after importing thumbor-aws:

```
############################## AWS Result Storage ##############################

## Region where thumbor's objects are going to be stored.
## Defaults to: 'us-east-1'
#AWS_RESULT_STORAGE_REGION_NAME = 'us-east-1'

## S3 Bucket where thumbor's objects are going to be stored.
## Defaults to: 'thumbor'
#AWS_RESULT_STORAGE_BUCKET_NAME = 'thumbor'

## Secret access key for S3 to allow thumbor to store objects there.
## Defaults to: None
#AWS_RESULT_STORAGE_S3_SECRET_ACCESS_KEY = None

## Access key ID for S3 to allow thumbor to store objects there.
## Defaults to: None
#AWS_RESULT_STORAGE_S3_ACCESS_KEY_ID = None

## Endpoint URL for S3 API. Very useful for testing.
## Defaults to: None
#AWS_RESULT_STORAGE_S3_ENDPOINT_URL = None

## Result Storage prefix path.
## Defaults to: '/rs'
#AWS_RESULT_STORAGE_ROOT_PATH = '/rs'

## ACL to use for storing items in S3.
## Defaults to: None
#AWS_RESULT_STORAGE_S3_ACL = None

################################################################################
```

### Configuring thumbor in compatibility mode with tc_aws

If you are a [tc_aws](https://github.com/thumbor-community/aws) user, thumbor-aws has a compatibility mode where you can use the same configuration you are already used to:

```python
############################# tc_aws Compatibility #############################

## Runs in compatibility mode using the configurations for tc_aws.
## Defaults to: False
THUMBOR_AWS_RUN_IN_COMPATIBILITY_MODE = True

## AWS Region the bucket is located in.
## Defaults to: 'us-east-1'
TC_AWS_REGION = 'us-east-1'

## Max retries for get image from S3 Bucket. Default is 0
## Defaults to: 0
TC_AWS_MAX_RETRY = 0  # This is not yet supported

## S3 bucket for Loader. If given, source urls are interpreted as keys within
## this bucket. If not given, source urls are expected to containthe bucket
## name, such as 's3-bucket/keypath'.
## Defaults to: ''
TC_AWS_LOADER_BUCKET = 'my-bucket'

## S3 path prefix for Loader bucket. If given, this is prefixed to all S3 keys.
## Defaults to: ''
TC_AWS_LOADER_ROOT_PATH = 'source-files'

## S3 bucket for Storage
## Defaults to: ''
TC_AWS_STORAGE_BUCKET = 'my-bucket'

## S3 path prefix for Storage bucket
## Defaults to: ''
TC_AWS_STORAGE_ROOT_PATH = 'source-files'

## put data into S3 using the Server Side Encryption functionality to encrypt
## data at rest in S3 https://aws.amazon.com/about-aws/whats-
## new/2011/10/04/amazon-s3-announces-server-side-encryption-support/
## Defaults to: False
TC_AWS_STORAGE_SSE = False  # This is not yet supported

## put data into S3 with Reduced Redundancy https://aws.amazon.com/about-
## aws/whats-new/2010/05/19/announcing-amazon-s3-reduced-redundancy-storage/
## Defaults to: False
TC_AWS_STORAGE_RRS = False  # This is not yet supported

## S3 bucket for result Storage
## Defaults to: ''
TC_AWS_RESULT_STORAGE_BUCKET = 'my-bucket'

## S3 path prefix for Result storage bucket
## Defaults to: ''
TC_AWS_RESULT_STORAGE_ROOT_PATH = 'result-storage'

## Store result with metadata (for instance content-type)
## Defaults to: False
# This configuration won't matter as thumbor-aws stores metadata anyway
TC_AWS_STORE_METADATA = False

################################################################################
```

Please notice the addition of `THUMBOR_AWS_RUN_IN_COMPATIBILITY_MODE = True` to tell `thumbor_aws` you want compatibility with `tc_aws`.

If you have any issues with this

#### Caveats

1. thumbor-aws does not create buckets for you. If they don't exist you are getting errors.

You can easily create a bucket using [aws-cli](https://aws.amazon.com/cli/?nc1=h_ls) with:

```
$ aws s3api create-bucket --bucket <bucket name> --region <your region>
```

Or through your [AWS Console UI](https://console.aws.amazon.com/s3/home?region=us-east-1).

### Troubles?

If you experience any troubles, try running:

```bash
thumbor-doctor
```

If you still need help, please [raise an issue](https://github.com/thumbor/thumbor-aws/issues).

## 👀 Thumbor

[thumbor-aws](https://github.com/thumbor/thumbor-aws) stands on the shoulders of [thumbor](https://github.com/thumbor/thumbor)! If you are not familiar with [thumbor](https://github.com/thumbor/thumbor), please check the [docs](https://thumbor.readthedocs.io/en/latest/) or you can see a demo at http://thumborize.me/

## 👍 Contribute

thumbor-aws is an open-source project with many contributors. Join them
[contributing code](https://github.com/thumbor/thumbor-aws/blob/master/CONTRIBUTING.md) or
[contributing documentation](https://github.com/thumbor/thumbor-aws/blob/master/CONTRIBUTING.md).

Join the chat at https://gitter.im/thumbor/thumbor

## License

MIT License

Copyright (c) 2021 thumbor-aws (by @heynemann)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
