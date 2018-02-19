from voyage.extensions import db
from voyage.utils import UUIDString, uuid4_str


class Voyage(db.Model):
    __tablename__ = 'voyages'

    id = db.Column(UUIDString, primary_key=True, default=uuid4_str)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<Voyage: {} ({})>".format(self.name, self.id)
