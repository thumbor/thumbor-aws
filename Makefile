PYTHON = python
.PHONY: docs build perf

OS := $(shell uname)

setup:
	@pip install -U pip
	@pip install -e .[tests]

services: docker-down
	@docker-compose up --remove-orphans

ci: docker-down docker-up
	@./wait-for-it.sh localhost:4566 -- echo "Docker Compose is Up. Running tests..."
	@coverage run -m pytest --cov=thumbor_aws -sv tests && coverage xml && mv coverage.xml cobertura.xml

docker-up:
	@docker-compose up --remove-orphan -d

docker-down:
	@docker-compose stop
	@docker-compose rm -f

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
