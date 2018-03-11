from sqlalchemy import func
from sqlalchemy.orm import validates
from sqlalchemy_utc import UtcDateTime

from voyage.exceptions import InvalidChapterException
from voyage.extensions import db
from voyage.utils import UUIDString, uuid4_str


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(UUIDString, primary_key=True, default=uuid4_str)
    created = db.Column(UtcDateTime, server_default=func.now())
    modified = db.Column(UtcDateTime, onupdate=func.now())

    user_id = db.Column(UUIDString, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')

    voyage_id = db.Column(UUIDString, db.ForeignKey('voyage.id'), nullable=False)
    voyage = db.relationship('Voyage')

    text = db.Column(db.String, nullable=False)
    chapter = db.Column(db.String, nullable=False)

    def __repr__(self):
        text = self.text if len(self.text) < 20 else "{}...".format(self.text[:17])
        return '<Comment: "{}" on chapter {} in {}>'.format(text, self.chapter, self.voyage.id)

    @validates('chapter')
    def validate_chapter(self, key, chapter):
        if chapter not in self.voyage.chapters:
            raise InvalidChapterException('Chapter {} is not a part of the voyage'.format(chapter))
        return chapter
