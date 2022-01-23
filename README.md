<p align="center">
<img src="https://raw.github.com/thumbor/thumbor/master/logo-thumbor.png" />
</p>

<h3 align="center">thumbor-aws</h3>

<p align="center">
This is a project to provide modern thumbor>7.0.0 AWS Extensions.
</p>

<p align="center">
  <img src='https://github.com/thumbor/thumbor-aws/workflows/build/badge.svg' />
  <a href='https://coveralls.io/github/thumbor/thumbor-aws?branch=master' target='_blank'>
    <img src='https://coveralls.io/repos/thumbor/thumbor-aws/badge.svg?branch=master&service=github'/>
  </a>
  <a href='https://codeclimate.com/github/thumbor/thumbor-aws' target='_blank'>
    <img src='https://codeclimate.com/github/thumbor/thumbor-aws/badges/gpa.svg'/>
  </a>
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

## Usage

### Configuring thumbor

Configure your `thumbor.conf` file to point to `thumbor_aws`:

```
## The file storage thumbor should use to store original images. This must be the
## full name of a python module (python must be able to import it)
## Defaults to: 'thumbor.storages.file_storage'
STORAGE = 'thumbor_aws.storage'

## The result storage thumbor should use to store generated images. This must be
## the full name of a python module (python must be able to import it)
## Defaults to: None
RESULT_STORAGE = 'thumbor_aws.result_storage'
```

As usual for thumbor, you don't need to use both at the same time. Feel free to use only what's needed.

### Configuration

thumbor-aws allows you to configure each storage independently, so there are configuration keys for each.

#### Storage

Below you can see the result of running thumbor's config generation after importing thumbor-aws:

```
################################# AWS Storage ##################################

## Region where thumbor's objects are going to be stored.
## Defaults to: 'us-east-1'
# AWS_STORAGE_REGION_NAME = 'us-east-1'

## S3 Bucket where thumbor's objects are going to be stored.
## Defaults to: 'thumbor'
# AWS_STORAGE_BUCKET_NAME = 'thumbor'

## Secret access key for S3 to allow thumbor to store objects there.
## Defaults to: None
# AWS_STORAGE_S3_SECRET_ACCESS_KEY = None

## Access key ID for S3 to allow thumbor to store objects there.
## Defaults to: None
# AWS_STORAGE_S3_ACCESS_KEY_ID = None

## Endpoint URL for S3 API. Very useful for testing.
## Defaults to: None
# AWS_STORAGE_S3_ENDPOINT_URL = None

## Endpoint URL for S3 API. Very useful for testing.
## Defaults to: None
# AWS_STORAGE_S3_ENDPOINT_URL = None

## Storage prefix path.
## Defaults to: '/st'
# AWS_STORAGE_ROOT_PATH = '/st'

## Storage ACL for files written in bucket
## Defaults to: 'public-read'
# AWS_STORAGE_S3_ACL = 'public-read'

################################################################################
```

#### Result Storage

Below you can see the result of running thumbor's config generation after importing thumbor-aws:

```
############################## AWS Result Storage ##############################

## Region where thumbor's objects are going to be stored.
## Defaults to: 'us-east-1'
# AWS_RESULT_STORAGE_REGION_NAME = 'us-east-1'

## S3 Bucket where thumbor's objects are going to be stored.
## Defaults to: 'thumbor'
# AWS_RESULT_STORAGE_BUCKET_NAME = 'thumbor'

## Secret access key for S3 to allow thumbor to store objects there.
## Defaults to: None
# AWS_RESULT_STORAGE_S3_SECRET_ACCESS_KEY = None

## Access key ID for S3 to allow thumbor to store objects there.
## Defaults to: None
# AWS_RESULT_STORAGE_S3_ACCESS_KEY_ID = None

## Endpoint URL for S3 API. Very useful for testing.
## Defaults to: None
# AWS_RESULT_STORAGE_S3_ENDPOINT_URL = None

## Result Storage prefix path.
## Defaults to: '/rs'
# AWS_RESULT_STORAGE_ROOT_PATH = '/rs'

## ACL to use for storing items in S3.
## Defaults to: None
# AWS_RESULT_STORAGE_S3_ACL = None

################################################################################
```

#### Caveats

1. thumbor-aws does not create buckets for you. If they don't exist you are getting errors.

### Troubles?

If you experience any troubles, try running:

```bash
thumbor-doctor
```

If you still need help, please [raise an issue](https://github.com/thumbor/thumbor-aws/issues).

## 🎯 Features

- Asynchronous non-blocking AWS S3 support
- Conforms with thumbor 7 new storage and results storage specs
- Python 3 compliant
- S3 Storage - Retrieve and store source files, detector data and security keys;
- S3 Result Storage - Retrieve and store resulting images. These can be set to be public-read and served directly from S3.

## 👍 Contribute

thumbor-aws is an open-source project with many contributors. Join them
[contributing code](https://github.com/thumbor/thumbor-aws/blob/master/CONTRIBUTING.md) or
[contributing documentation](https://github.com/thumbor/thumbor-aws/blob/master/CONTRIBUTING.md).

Join the chat at https://gitter.im/thumbor/thumbor

## 👀 Demo

You can see thumbor in action at http://thumborize.me/

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
