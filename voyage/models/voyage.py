from sqlalchemy.orm import relationship

from voyage.extensions import db
from voyage.utils import UUIDString, uuid4_str


class Voyage(db.Model):
    __tablename__ = 'voyages'

    id = db.Column(UUIDString, primary_key=True, default=uuid4_str)
    name = db.Column(db.String, nullable=False)

    media_id = db.Column(UUIDString, db.ForeignKey('media.id'), nullable=False)
    media = relationship('Media')

    def __repr__(self):
        return "<Voyage: {} ({})>".format(self.name, self.id)
