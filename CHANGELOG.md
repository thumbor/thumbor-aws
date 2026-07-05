# Changelog

## [1.1.1](https://github.com/thumbor/thumbor-aws/compare/v1.1.0...v1.1.1) (2026-07-05)


### Bug Fixes

* never store the security key with a public ACL ([#392](https://github.com/thumbor/thumbor-aws/issues/392)) ([5143470](https://github.com/thumbor/thumbor-aws/commit/514347030547d33a8004c2384a93ea5dd09960ff))
* return bytes and correct log message on get_data errors ([abe6c51](https://github.com/thumbor/thumbor-aws/commit/abe6c5103a0d5808d0a592a21d985c0bea7784d1))
* run stale workflow once every six hours instead of every minute ([349e698](https://github.com/thumbor/thumbor-aws/commit/349e698625c889f4c2590109ba0a36a03c2ec2a9))


### Documentation

* warn about URL-controlled bucket selection in the loader ([16e2382](https://github.com/thumbor/thumbor-aws/commit/16e2382ee6adf2b89af80c70e01a52bd36ec6d23))

## [1.1.0](https://github.com/thumbor/thumbor-aws/compare/v1.0.0...v1.1.0) (2026-06-25)


### Features

* **release:** add PyPI attestation via trusted publishing ([#386](https://github.com/thumbor/thumbor-aws/issues/386)) ([93fa26e](https://github.com/thumbor/thumbor-aws/commit/93fa26e843353548ffebc305595aa4d94464506f))


### Bug Fixes

* **s3_client:** fallback to application/octet-stream when content_type is None ([#383](https://github.com/thumbor/thumbor-aws/issues/383)) ([365a2be](https://github.com/thumbor/thumbor-aws/commit/365a2be4301dfbfd79a316dc7f38350a95d17a60)), closes [#375](https://github.com/thumbor/thumbor-aws/issues/375)

## [1.0.0](https://github.com/thumbor/thumbor-aws/compare/v0.9.1...v1.0.0) (2026-06-05)


### ⚠ BREAKING CHANGES

* Drop support to Python 3.9 ([#344](https://github.com/thumbor/thumbor-aws/issues/344))

### Features

* Drop support to Python 3.9 ([#344](https://github.com/thumbor/thumbor-aws/issues/344)) ([8d3863f](https://github.com/thumbor/thumbor-aws/commit/8d3863f85d9d7b58f87c6629021a28bb21b07066))


### Documentation

* Update loader configuration in README ([#367](https://github.com/thumbor/thumbor-aws/issues/367)) ([5e66f20](https://github.com/thumbor/thumbor-aws/commit/5e66f20bad190568907b9a1ad2825ab2a3fa5e5c))

## [0.9.1](https://github.com/thumbor/thumbor-aws/compare/v0.9.0...v0.9.1) (2025-08-26)


### Bug Fixes

* Move the `AWS_NORMALIZER` config to top-level configuration list ([#316](https://github.com/thumbor/thumbor-aws/issues/316)) ([375414a](https://github.com/thumbor/thumbor-aws/commit/375414aa2b8ccd963d443d763637d92792ab74d9))

## [0.9.0](https://github.com/thumbor/thumbor-aws/compare/v0.8.1...v0.9.0) (2025-08-23)


### Features

* Drop support to Python 3.8 ([#297](https://github.com/thumbor/thumbor-aws/issues/297)) ([e1db6f2](https://github.com/thumbor/thumbor-aws/commit/e1db6f2141306ac208fab46ea1f0d2643c1f5cbe))


### Bug Fixes

* Connection leak reported on [#113](https://github.com/thumbor/thumbor-aws/issues/113) ([#315](https://github.com/thumbor/thumbor-aws/issues/315)) ([cf75d9f](https://github.com/thumbor/thumbor-aws/commit/cf75d9f59ad96d820859c4a7671bd62f9329e6a9))
* GH action release tag match ([ef436e9](https://github.com/thumbor/thumbor-aws/commit/ef436e92dcd86815c94af674ef61a90d69ca023b))

## [0.8.1](https://github.com/thumbor/thumbor-aws/compare/0.8.0...v0.8.1) (2024-09-02)


### Bug Fixes

* release-please ([97e3def](https://github.com/thumbor/thumbor-aws/commit/97e3defdbcfdb070a3e08a402644ec7d58e32248))
* release-please use PAT ([4ea28a6](https://github.com/thumbor/thumbor-aws/commit/4ea28a65a1ccac7d8e227f397256201b82f0ef78))


### Documentation

* Add Conventional commits to CONTRIBUTING.md ([e8331ff](https://github.com/thumbor/thumbor-aws/commit/e8331ff9250faab7cee15d6dac97bebf2ae1f0e0))
