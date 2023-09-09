install:
	python -m pip install --upgrade pip
	python -m pip install -e .

install-dev: install
	python -m pip install -e ".[dev]"

build: 
	pip-compile --resolver=backtracking --output-file=requirements.txt pyproject.toml
	pip-compile --resolver=backtracking --extra=dev --output-file=requirements-dev.txt pyproject.toml

format:
	isort .
	black .

check:
	ruff .
	isort --check . 
	black --check .

test:
	pytest -v