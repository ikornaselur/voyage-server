from flask import redirect, url_for
from flask_login import LoginManager, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


def configure_extensions(app):
    db.init_app(app)
    setup_login_manager(app)


def setup_login_manager(app):
    login_manager.setup_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from voyage.models import User
        return User.query.get(user_id)

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('google.login'))

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect('/')
