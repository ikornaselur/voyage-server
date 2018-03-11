from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from sqlalchemy import func
from sqlalchemy_utc import UtcDateTime

from voyage.extensions import db
from voyage.utils import UUIDString, uuid4_str


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(UUIDString, primary_key=True, default=uuid4_str)
    created = db.Column(UtcDateTime, server_default=func.now())
    modified = db.Column(UtcDateTime, onupdate=func.now())

    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    profile_picture = db.Column(db.String)

    def __repr__(self):
        return "<User: {} ({})>".format(self.name, self.email)

    @property
    def voyages(self):
        from voyage.models import Membership, Voyage
        return (
            Voyage.query
            .join(Membership)
            .filter(
                Membership.user == self,
            )
        ).all()


class OAuth(OAuthConsumerMixin, db.Model):
    """ OAuth entry

    The OAuthConsumerMixin provides:
        id (int)
        provider (string)
        created_at (datetime)
        token (json)
    """
    provider_user_id = db.Column(db.String(256), unique=True)

    user_id = db.Column(UUIDString, db.ForeignKey(User.id))
    user = db.relationship(User, backref='oauth')
