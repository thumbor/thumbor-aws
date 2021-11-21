PYTHON = python
.PHONY: docs build perf

OS := $(shell uname)

setup:
	@$(PYTHON) -m pip install -e .[tests]

test:
	@$(MAKE) unit coverage
	@$(MAKE) integration_run
	@$(MAKE) flake
	@$(MAKE) kill_redis

unit:
	@pytest --cov=thumbor_aws tests/

sequential-unit:
	@pytest -sv --junit-xml=test-results/unit/results.xml --cov=thumbor_aws tests/

format:
	@black .

flake:
	@flake8 --config flake8

pylint:
	@pylint thumbor tests
