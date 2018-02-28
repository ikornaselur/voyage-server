POSTGRES_PORT = 15432
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

# Start a postgres docker and expose it on port the configured port
postgres_docker_init:
	@docker container inspect ${POSTGRES_DOCKER_NAME} &>/dev/null \
		|| docker run -d --name ${POSTGRES_DOCKER_NAME} -p $(POSTGRES_PORT):5432 postgres

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
database_init: postgres
	pipenv run python init_db.py

# Connect to postgres
pg:
	pipenv run pgcli -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U voyage voyage

# Open a ipython shell with the application context
shell:
	pipenv run python manage.py shell

# Lint
lint:
	pipenv run flake8 voyage
	pipenv run isort -c -df -rc voyage

# Run all tests
test:
	PIPENV_DOTENV_LOCATION=$(shell pwd)/.env.test pipenv run py.test tests/

# Run all tests, without capturing output
test_debug:
	PIPENV_DOTENV_LOCATION=$(shell pwd)/.env.test pipenv run py.test tests/ -vv -s --ff -x

# Update all test snapshots
update_snapshots:
	PIPENV_DOTENV_LOCATION=$(shell pwd)/.env.test pipenv run py.test tests/ --snapshot-update

# Bootstrap the project, set up env and database
bootstrap: venv postgres_init database_init
