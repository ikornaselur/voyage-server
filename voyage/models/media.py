from sqlalchemy import func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy_utc import UtcDateTime

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
    created = db.Column(UtcDateTime, server_default=func.now())
    modified = db.Column(UtcDateTime, onupdate=func.now())

    series = db.Column(db.String, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)

    type = db.Column(db.String, nullable=False)
    chapters = db.Column(MutableList.as_mutable(ARRAY(db.String)))  # Assume books for now

    # thetvdb.com or goodreads.com
    external_url = db.Column(db.String)

    def __init__(self, series, order, name, type, chapters, external_url=None):
        self.series = series
        self.order = order
        self.name = name
        self.type = type
        self.external_url = external_url
        self.chapters = [str(c) for c in chapters]  # Ensure the chapters are a list of strings

    def __repr__(self):
        return "<Media: {} ({})>".format(self.name, self.id)
