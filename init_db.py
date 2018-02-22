from voyage.app import create_app
from voyage.extensions import db

if __name__ == "__main__":
    with create_app().app_context():
        db.drop_all()
        db.create_all()
