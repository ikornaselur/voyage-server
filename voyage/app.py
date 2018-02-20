import os

from flask import Flask
from flask_dance.contrib.google import make_google_blueprint
from flask_graphql import GraphQLView
from werkzeug.contrib.fixers import ProxyFix

from voyage.schema import schema


def create_app():
    app = Flask('voyage')
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.secret_key = os.environ.get('FLASK_SECRET', 's3cr3t')
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
    app.register_blueprint(
        make_google_blueprint(
            client_id=os.environ['GOOGLE_CLIENT_ID'],
            client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
            scope=['profile', 'email'],
        ),
        url_prefix='/login',
    )

    return app
