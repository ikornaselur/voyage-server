import os

from flask import Flask, make_response
from flask_graphql import GraphQLView
from flask_login import login_required
from werkzeug.contrib.fixers import ProxyFix


ENABLE_SUBSCRIPTIONS = os.environ.get('DISABLE_SUBSCRIPTIONS') is None


def create_app(testing=False):
    if ENABLE_SUBSCRIPTIONS:
        from gevent.monkey import patch_all
        patch_all()
        from psycogreen.gevent import patch_psycopg
        patch_psycopg()

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
                allow_subscriptions=ENABLE_SUBSCRIPTIONS,
            )
        )
    )

    @app.route('/graphiql')
    @login_required
    def graphiql_view():
        from voyage.graphiql import render_graphiql
        return make_response(render_graphiql(enable_subscriptions=ENABLE_SUBSCRIPTIONS))

    if not testing:
        if os.environ.get('LOCAL_AUTH', False):
            # Just set up local auth
            from voyage.auth import local_auth
            local_auth(app)
        else:
            from voyage.auth import google_auth
            google_auth(app)

    from voyage.extensions import configure_extensions
    configure_extensions(app)

    return app
