from flask import Flask
from flask_graphql import GraphQLView

from voyage.schema import schema


def create_app():
    app = Flask('voyage')

    app.add_url_rule(
        '/',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True,
        )
    )

    return app


application = create_app()
