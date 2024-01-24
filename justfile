set windows-shell := ["C:\\Program Files\\Git\\bin\\sh.exe", "-c"]

_default: tasks

# List tasks
tasks:
	@just --list --unsorted

_setup_poetry:
	@poetry install

# SetUp project
setup: _setup_poetry
	(just mypy 2> /dev/null ; yes | poetry run mypy --install-types)
	@poetry run pre-commit install

# Run ipython
ipython:
	@poetry run ipython

# Run 'ruff'
ruff *args:
	@poetry run ruff {{ args }} .

# Run organize imports and format all code
format:
	@just ruff check --select I --fix
	@just ruff format

# Run mypy
mypy *args:
	@poetry run mypy {{ args }} .

# Lint code
lint: format
	@just ruff check
	@just mypy

# 'ruff --fix'
ruff-fix:
	@just ruff --fix

# Format and Lint code, and validate poetry 
check: format lint
	@poetry check

# Run
run *args:
    @poetry run pyproject-cli {{ args }}

# Update the Usage img in README.md
_update_readme:
	COLUMNS=$(COLUMNS=$(tput cols) just run --help | head -n 1 | wc -c) just run --make-help-preview

# Build project
build: _setup_poetry
	@just _update_readme
	@poetry build

# Install program using pipx
install: build
	@py -m pipx install ./dist/`ls -t dist | head -n2 | grep whl`

# Uninstall program using pipx
uninstall:
	@py -m pipx uninstall pyproject-cli

# Reinstall program using pipx
reinstall: uninstall
	@just install