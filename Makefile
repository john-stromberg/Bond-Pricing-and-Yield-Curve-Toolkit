.PHONY: install lint format test

install:
	poetry install

lint:
	poetry run ruff check .
	poetry run black --check .

format:
	poetry run black .
	poetry run ruff check --fix .

test:
	poetry run pytest
