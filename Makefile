.PHONY: all help lock install test publish build

all: help
	@ echo "Usage:"
	@ echo " make lock"

lock:
	poetry lock

install-dev:
	poetry install --no-root --with dev

install:
	poetry install --no-root

add-dev:
	poetry add $(PACKAGE) --group dev

add:
	poetry add $(PACKAGE)

build:
	poetry build

unit-test:
	poetry run pytest tests/unit

integration-test:
	poetry run pytest tests/integration

publish:
	export POETRY_REPOSITORIES_PUBLISH_URL="placeholder"
	export POETRY_HTTP_BASIC_PUBLISH_USERNAME="placeholder"
	export POETRY_HTTP_BASIC_PUBLISH_PASSWORD="placeholder"
	poetry publish --build -r publish
