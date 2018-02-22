from voyage.extensions import db
from voyage.models.many_to_many import voyage_members_table
from voyage.utils import UUIDString, uuid4_str


class Voyage(db.Model):
    __tablename__ = 'voyage'

    id = db.Column(UUIDString, primary_key=True, default=uuid4_str)
    name = db.Column(db.String, nullable=False)

    media_id = db.Column(UUIDString, db.ForeignKey('media.id'), nullable=False)
    media = db.relationship('Media')

    owner_id = db.Column(UUIDString, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User')

    members = db.relationship('User', secondary=voyage_members_table, lazy='joined')

    def __repr__(self):
        return "<Voyage: {} ({})>".format(self.name, self.id)
