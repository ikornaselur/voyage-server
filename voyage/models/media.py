from sqlalchemy.dialects.postgresql import ARRAY

from voyage.extensions import db
from voyage.utils import MutableList, UUIDString, uuid4_str


class Media(db.Model):
    """ A media entry

    All voyages reference a media.

    An example of a tv show media:
        series: Game of Thrones
        order: 3
        name: Season 3

    An example of a book media:
        series: Stormlight Archive
        order: 2
        name: Words of Radiance
    """
    __tablename__ = 'media'

    id = db.Column(UUIDString, primary_key=True, default=uuid4_str)

    series = db.Column(db.String, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)

    type = db.Column(db.String, nullable=False)
    chapters = db.Column(MutableList.as_mutable(ARRAY(db.String)))  # Assume books for now

    # thetvdb.com or goodreads.com
    external_url = db.Column(db.String)

    def __repr__(self):
        return "<Media: {} ({})>".format(self.name, self.id)
