POSTGRES_PORT = 5432
POSTGRES_HOST = "localhost"
POSTGRES_DOCKER_NAME = "postgres_voyage"


# Setup project dependencies
dependencies:
	pip install pipenv

# Setup a virtualenv for the project using pipenv
venv: dependencies
	pipenv install --dev

# Run the gevent server
server:
	pipenv run python server.py

# Run the flask dev server
# Will disable subscriptions, since they require running the gevent server
# The dev server is recommended (for now) when not developing anything related
# to subscriptions, since it supports reloading on code changes
dev_server:
	DISABLE_SUBSCRIPTIONS=1 FLASK_APP=voyage/application.py FLASK_DEBUG=1 pipenv run flask run -p 9999 --host 0.0.0.0

# Start a postgres docker and expose it on port the configured port
postgres_docker_init:
	@docker container inspect ${POSTGRES_DOCKER_NAME} &>/dev/null \
		|| docker run -d --name ${POSTGRES_DOCKER_NAME} -p $(POSTGRES_PORT):5432 postgres:10.2

# Start the postgres docker
postgres: postgres_docker_init
	@docker start ${POSTGRES_DOCKER_NAME}

# Initialize postgres
postgres_init: postgres
	@sleep 5
	-createuser -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U postgres voyage
	-createdb -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U postgres -O voyage voyage
	-createdb -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U postgres -O voyage voyage_test

# Init DB
# Makes sure postgres is running and then runs init_db.py
database_init: postgres
	pipenv run python init_db.py

# Create some test fixtures in the local database
fixtures:
	pipenv run python fixtures.py

# Connect to postgres
pg:
	pipenv run pgcli -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U voyage voyage

# Open a ipython shell with the application context
shell:
	DISABLE_PSYCOGREEN=1 pipenv run python manage.py shell

# Lint
lint:
	pipenv run flake8 voyage tests
	pipenv run isort -c -df -rc voyage tests

# Run all tests
test:
	PIPENV_DOTENV_LOCATION=$(shell pwd)/.env.test pipenv run py.test tests/

# Run all tests, without capturing output
test_debug:
	PIPENV_DOTENV_LOCATION=$(shell pwd)/.env.test pipenv run py.test tests/ -vv -s --ff -x

# Bootstrap the project, set up env and database
bootstrap: venv postgres_init database_init
