import os

from flask import Flask
from flask_graphql import GraphQLView

from voyage.schema import schema


def create_app():
    app = Flask('voyage')

    app.config.update({
        'SQLALCHEMY_DATABASE_URI': os.environ['SQLALCHEMY_DATABASE_URI'],
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    from .extensions import configure_extensions
    configure_extensions(app)

    app.add_url_rule(
        '/',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True,
        )
    )

    return app
