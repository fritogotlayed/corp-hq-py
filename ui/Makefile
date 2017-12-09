# Don't forget that make must have tabs...
# @ suppresses the normal 'echo' of the command that is executed
# - ignores the exit status of the command that is executed (normally non-zero would halt execution)
# + executes "make -n"
.DEFAULT_GOAL := help
.PHONY: test

analysis:  ## Runs the static code analysis tool
	@npm run lint

compose-rebuild:  ## Rebuilds the UI then rebuilds the docker compose stack
	@npm run build
	@docker-compose build

compose-up:  ## Rebuilds the app stack containers then starts them
	@docker-compose up --build -d

docker-image:  ## Builds the current source as a tag to the latest image.
	@npm run build
	@docker build -t corp-hq-ui:latest .

help:  ## Prints this help message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:  ## Installs the app in a way that modifications to the files are run easily
	@npm install

mongo:  ## Starts only the mondo docker container. Useful when running both -ui and -api locally
	@docker-compose up -d mongodb

run-docker:  ## Runs the latest tag for the corp-hq-ui
	docker run -d -p 80:80 corp-hq-ui:latest

test:  ## Runs the unit tests and end to end tests
	@npm run test

test-e2e:  ## Runs the unit tests and end to end tests
	@npm run e2e

test-unit:  ## Runs the unit tests and end to end tests
	@npm run unit
