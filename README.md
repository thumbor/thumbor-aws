# thumbor-aws

This is a project to provide modern thumbor>7.0.0 AWS Extensions.

At this point the following are supported:

* S3 Storage - Retrieve and store source files from an S3 bucket and use them in thumbor for transforming images, as well as storing detector data and security keys for each file;
* S3 Result Storage - Retrieve and store resulting images to avoid recalculating them.

In the future there are plans of adding support for other AWS services.

## Usage

Using thumbor-aws is simple. Install it using `pip install thumbor-aws` (or add the dependency to your library, requirements.txt or setup.py) and add the following configuration to your `thumbor.conf`:

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

## Configuration

thumbor-aws allows you to configure each storage independently, so there are configuration keys for each.

### Storage

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

## ACL to use for storing items in S3.
## Defaults to: None
#AWS_STORAGE_S3_ACL = None

################################################################################
```

### Result Storage

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

## Hacking

## License

MIT License

Copyright (c) 2021 Thumbor (by @globocom)

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
