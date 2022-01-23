PYTHON = python
.PHONY: docs build perf

OS := $(shell uname)

setup:
	@$(PYTHON) -m pip install -e .[tests]

services:
	@docker-compose up

ci:
	@docker-compose up -d
	@./wait-for-it.sh localhost:4566 -- echo "Docker Compose is Up. Running tests..."
	@pytest -sv --junit-xml=test-results/unit/results.xml --cov=thumbor_aws tests/

test:
	@$(MAKE) unit
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

publish:
	@python setup.py sdist
	@twine upload dist/*
	@rm -rf dist/
