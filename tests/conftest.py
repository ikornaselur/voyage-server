from contextlib import contextmanager

import pytest
from flask.testing import FlaskClient
from flask_login import login_user

from voyage.app import create_app
from voyage.extensions import db as _db
from voyage.models import Media, User, Voyage


class TestClient(FlaskClient):
    @contextmanager
    def use(self, user):
        login_user(user)
        yield

    def open(self, *args, **kwargs):
        pass


@pytest.fixture(scope='session')
def app():
    app = create_app(testing=True)
    app.test_client_class = TestClient
    with app.test_request_context():
        yield app


@pytest.yield_fixture(scope='function')
def db_session(app):
    _db.create_all()
    _db.session.begin_nested()
    yield _db.session
    _db.session.rollback()
    _db.drop_all()


@pytest.yield_fixture(scope='function')
def db_media(db_session):
    media = Media(
        series='series',
        order=1,
        name='name',
        type='book',
        chapters=['1', '2'],
        external_url='http://example.com'
    )
    db_session.add(media)
    db_session.commit()

    yield media


@pytest.yield_fixture(scope='function')
def db_user(db_session):
    user = User(
        name='Normal User',
        email='normal@example.com',
    )
    db_session.add(user)
    db_session.commit()

    yield user


@pytest.yield_fixture(scope='function')
def db_user_owner(db_session):
    user = User(
        name='Owner User',
        email='owner@example.com',
    )
    db_session.add(user)
    db_session.commit()

    yield user


@pytest.yield_fixture(scope='function')
def db_user_member(db_session):
    user = User(
        name='Member User',
        email='member@example.com',
    )
    db_session.add(user)
    db_session.commit()

    yield user


@pytest.yield_fixture(scope='function')
def db_voyage(db_session, db_media, db_user_owner, db_user_member):
    voyage = Voyage(
        name='The Voyage',
        media=db_media,
        owner=db_user_owner,
        members=[db_user_owner, db_user_member],
    )
    db_session.add(voyage)
    db_session.commit()

    yield voyage


@pytest.yield_fixture(scope='function')
def client(app):
    yield app.test_client()
