import os

from flask import Flask
from flask_graphql import GraphQLView
from flask_login import login_required
from werkzeug.contrib.fixers import ProxyFix


def create_app():
    app = Flask('voyage')
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.secret_key = os.environ.get('FLASK_SECRET', 's3cr3t')
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': os.environ['SQLALCHEMY_DATABASE_URI'],
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    from voyage.schema import schema
    app.add_url_rule(
        '/',
        view_func=login_required(
            GraphQLView.as_view(
                'graphql',
                schema=schema,
                graphiql=True,
            )
        )
    )

    from .extensions import configure_extensions
    configure_extensions(app)

    return app
