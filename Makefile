PYTHON = python
.PHONY: docs build perf

OS := $(shell uname)

setup:
	@$(PYTHON) -m pip install -e .[tests]

services:
	@docker run --rm -it -p 4566:4566 -p 4571:4571 -e"SERVICES=s3" localstack/localstack

test:
	@$(MAKE) unit coverage
	@$(MAKE) flake

unit:
	@pytest --cov=thumbor_aws tests/

sequential-unit:
	@pytest -sv --junit-xml=test-results/unit/results.xml --cov=thumbor_aws tests/

format:
	@black .

flake:
	@flake8 --config .flake8

pylint:
	@pylint thumbor_aws tests

run:
	@thumbor -c thumbor.conf -l debug
