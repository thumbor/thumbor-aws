PYTHON = python
.PHONY: docs build perf

OS := $(shell uname)

setup:
	@pip install -U pip
	@poetry install

services: docker-down
	@docker-compose up --remove-orphans

ci:
	@poetry run coverage run -m pytest tests && coverage xml && mv coverage.xml cobertura.xml

docker-up:
	@docker-compose up --remove-orphan -d

docker-down:
	@docker-compose stop
	@docker-compose rm -f

test:
	@$(MAKE) unit
	@$(MAKE) flake

unit:
	@poetry run pytest --cov=thumbor_aws tests/

sequential-unit:
	@poetry run pytest -sv --junit-xml=test-results/unit/results.xml --cov=thumbor_aws tests/

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
