# Voyage Server

The backend for Voyage

## Development

### Dependencies

While not required, the make targets assume you have docker installed for
things such as postgres. If you don't want to use docker, you can manually set
up postgres, following the targets to see what's required.

### Getting started

You can get quickly quickly up and running with the following make targets:

```
make venv
make postgres
```

#### venv
Will make sure `pipenv` is installed before using it to install the environment

#### postgres
Will create a docker container named `postgres_voyage`, create a `voyage`
database and user. Initializes the database based on the models.
