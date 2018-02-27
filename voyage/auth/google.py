import os

from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.contrib.google import make_google_blueprint
from flask_login import current_user, login_user

from voyage.extensions import db
from voyage.models import OAuth, User

blueprint = make_google_blueprint(
    client_id=os.environ['GOOGLE_CLIENT_ID'],
    client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
    scope=['profile', 'email'],
)


def google_auth(app):
    """ Hook up google oauth authentication """
    app.register_blueprint(blueprint, url_prefix='/login')
    blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)


@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        return False

    resp = blueprint.session.get('/oauth2/v2/userinfo')
    if not resp.ok:
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

    # Disable Flask-Dance's default behaviour for saving the token
    return False


@oauth_error.connect_via(blueprint)
def google_error(blueprint, error, error_description=None, error_uri=None):
    print("Error?")
