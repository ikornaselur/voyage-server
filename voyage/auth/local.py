import os
import random

from flask import redirect
from flask_login import login_user


def local_auth(app):
    @app.route('/login/local')
    def login_local():
        from voyage.models import User
        from voyage.extensions import db

        email = os.environ.get('LOCAL_EMAIL')
        if not email:
            raise Exception('LOCAL_EMAIL env var not set')

        user = User.query.filter(User.email == email).first()
        if user is None:
            user = User(
                name='Test User',
                email=email,
                profile_picture='https://robohash.org/{}.png?bgset=bg1&set=set4'.format(random.random()),
            )
            db.session.add(user)
            db.session.commit()

        login_user(user)
        return redirect('/graphiql')
