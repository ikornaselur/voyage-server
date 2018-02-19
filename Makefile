# Setup project dependencies
dependencies:
	pip install pipenv

# Setup a virtualenv for the project using pipenv
venv: dependencies
	pipenv install

# Run the dev server
server:
	FLASK_APP=voyage/app.py FLASK_DEBUG=1 pipenv run flask run -p 9999 --host 0.0.0.0
