from sqlalchemy import Table

from voyage.extensions import db
from voyage.utils import UUIDString

voyage_members_table = Table(
    'voyage_members',
    db.Model.metadata,
    db.Column('voyage_id', UUIDString, db.ForeignKey('voyage.id', ondelete='cascade'), primary_key=True),
    db.Column('user_id', UUIDString, db.ForeignKey('user.id', ondelete='cascade'), primary_key=True),
)
