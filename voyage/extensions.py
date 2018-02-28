import os

from flask import redirect, url_for
from flask_login import LoginManager, login_required, logout_user
from flask_sockets import Sockets
from flask_sqlalchemy import SQLAlchemy
from graphql_ws.gevent import GeventSubscriptionServer

db = SQLAlchemy()
login_manager = LoginManager()


def configure_extensions(app):
    db.init_app(app)

    setup_login_manager(app)
    setup_subscription_server(app)


def setup_login_manager(app):
    login_manager.setup_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from voyage.models import User
        return User.query.get(user_id)

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        if os.environ.get('LOCAL_AUTH'):
            return redirect(url_for('login_local'))
        return redirect(url_for('google.login'))

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect('/')


def setup_subscription_server(app):
    from voyage.schema import schema

    sockets = Sockets(app)
    subscription_server = GeventSubscriptionServer(schema)
    app.app_protocol = lambda environ_path_info: 'graphql-ws'

    @sockets.route('/subscriptions')
    def echo_socket(ws):
        subscription_server.handle(ws)
        return []
