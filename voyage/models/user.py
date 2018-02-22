from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin

from voyage.extensions import db
from voyage.models.many_to_many import voyage_members_table
from voyage.utils import UUIDString, uuid4_str


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(UUIDString, primary_key=True, default=uuid4_str)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    profile_picture = db.Column(db.String)

    voyages = db.relationship('Voyage', secondary=voyage_members_table, lazy='joined')

    def __repr__(self):
        return "<User: {} ({})>".format(self.name, self.email)


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
