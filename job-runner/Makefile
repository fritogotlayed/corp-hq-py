# Don't forget that make must have tabs...
# See about moving this to Paver or Bolt to help support our windows friends
# https://pythonhosted.org/Paver/
# http://bolt-task-automation.readthedocs.io/en/latest/
basepython = python3.5
.DEFAULT_GOAL := help

VIRTUALENV = virtualenv --python=python3.5
VENV = .venv
VENV_ACTIVATE = . $(VENV)/bin/activate

analysis:  ## Runs the static code analysis tool
	-tox -r -elint-py3

check-deps:  ## Checks the pip requirements for out of date packages
	@pip list --outdated --format=columns

clean-pyc:  ## Cleans the environment of pyc, pyo and ~ files.
	@echo "Cleaning up pycaches..."
	@find . -name '*.pyc' -exec rm --force {} +
	@find . -name '*.pyo' -exec rm --force {} +
	@find . -name '*~' -exec rm --force {} +
	@echo "done."

create-venv:  ## Creates a virtual environment for the project
	virtualenv --python=python3 .venv

dev-install:  ## Installs the app in a way that modifications to the files are run easily
	@pip install -e .
	@pip install -r requirements_dev.txt

docker-image: test clean-pyc  ## Builds the current source as a tag to the latest image.
	@docker build -t corp-hq-api:latest .

help:  ## Prints this help message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

pretty:  ## Runs the python formatting tool against the code
	@echo "Making things pretty..."
	@yapf -i -r setup.py main.py developer.py ./tests/ ./api/
	@echo "done."

run:  # Runs the local version of the code for development
	$(VENV_ACTIVATE); corp-hq-api-server

run-docker:  ## Runs the latest tag for the corp-hq-ui
	docker run -d -p 8888:80 corp-hq-api:latest

test:  ## Runs the tox suite against each of the target interpreters.
	$(VENV_ACTIVATE); detox -r
