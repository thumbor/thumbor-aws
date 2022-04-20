PYTHON = python
.PHONY: docs build perf

OS := $(shell uname)

setup:
	@pip install -U pip
	@poetry install

services: docker-down
	@docker-compose up

coverage:
	@poetry run coverage report -m --fail-under=75
	@poetry run coverage lcov

ci: unit coverage

docker-up:
	@docker-compose up -d

docker-down:
	@docker-compose stop
	@docker-compose rm -f

test:
	@$(MAKE) unit
	@$(MAKE) flake

unit:
	@poetry run pytest --cov=thumbor_aws tests/

sequential-unit:
	@poetry run pytest -sv --cov=thumbor_aws tests/

format:
	@poetry run  black .

flake:
	@poetry run  flake8 --config .flake8

pylint:
	@poetry run  pylint thumbor_aws tests

run:
	@poetry run  thumbor -c thumbor.conf -l debug

publish:
	@poetry publish --build
