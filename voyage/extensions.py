from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def configure_extensions(app):
    db.init_app(app)
