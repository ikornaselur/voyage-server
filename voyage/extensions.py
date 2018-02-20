import os

from flask import redirect, url_for
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.contrib.google import make_google_blueprint
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
google_bp = make_google_blueprint(
    client_id=os.environ['GOOGLE_CLIENT_ID'],
    client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
    scope=['profile', 'email'],
)


def configure_extensions(app):
    from voyage.models import OAuth
    app.register_blueprint(google_bp, url_prefix='/login')
    google_bp.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

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


@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    from voyage.models import OAuth, User
    if not token:
        print("Token missing")
        return False

    resp = blueprint.session.get('/oauth2/v2/userinfo')
    if not resp.ok:
        print("Unable to get user info")
        return False

    google_info = resp.json()
    google_user_id = google_info['id']

    oauth = OAuth.query.filter(
        OAuth.provider == blueprint.name,
        OAuth.provider_user_id == google_user_id,
    ).one_or_none()

    if not oauth:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=google_user_id,
            token=token,
        )

    if oauth.user:
        login_user(oauth.user)
        print("Successfully logged in")
    else:
        user = User(
            name=google_info['name'],
            email=google_info['email'],
            profile_picture=google_info['picture'],
        )
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()

        login_user(user)
        print("Successfully created user and logged in")

    # Disable Flask-Dance's default behaviour for saving the token
    return False


@oauth_error.connect_via(google_bp)
def google_error(blueprint, error, error_description=None, error_uri=None):
    print("Error?")
