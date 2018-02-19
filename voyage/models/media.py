from sqlalchemy.dialects.postgresql import ARRAY

from voyage.extensions import db
from voyage.utils import MutableList, UUIDString, uuid4_str


class Media(db.Model):
    __tablename__ = 'media'

    id = db.Column(UUIDString, primary_key=True, default=uuid4_str)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    chapters = db.Column(MutableList.as_mutable(ARRAY(db.String)))  # Assume books for now

    def __repr__(self):
        return "<Media: {} ({})>".format(self.name, self.id)
