POSTGRES_PORT = 15432
POSTGRES_HOST = "localhost"
POSTGRES_DOCKER_NAME = "postgres_voyage"


# Setup project dependencies
dependencies:
	pip install pipenv

# Setup a virtualenv for the project using pipenv
venv: dependencies
	pipenv install

# Run the dev server
server:
	FLASK_APP=voyage/application.py FLASK_DEBUG=1 pipenv run flask run -p 9999 --host 0.0.0.0

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

# Init DB
database_init: postgres
	pipenv run python init_db.py

# Connect to postgres
pg:
	pipenv run pgcli -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U voyage voyage

# Open a ipython shell with the application context
shell:
	pipenv run python manage.py shell
