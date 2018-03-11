from sqlalchemy.orm import validates

from voyage.exceptions import InvalidChapterException, InvalidRoleException
from voyage.extensions import db
from voyage.utils import UUIDString, uuid4_str

ROLES = ['owner', 'member']


class Membership(db.Model):
    """ User membership in a voyage

    Tracks the user progres in the voyage
    """
    __tablename__ = 'voyage_user_membership'

    id = db.Column(UUIDString, primary_key=True, default=uuid4_str)

    voyage_id = db.Column(UUIDString, db.ForeignKey('voyage.id'), nullable=False)
    voyage = db.relationship('Voyage', backref='memberships')

    user_id = db.Column(UUIDString, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='memberships')

    active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String, default='member')

    current_chapter = db.Column('current_chapter', db.String, nullable=False)

    def __init__(self, user, voyage, role=None, current_chapter=None):
        self.user = user
        self.voyage = voyage

        if role:
            self.role = role

        if current_chapter:
            self.current_chapter = current_chapter
        else:
            self.current_chapter = voyage.chapters[0]

    def __repr__(self):
        return "<Membership: User '{}' in Voyage '{}' ({})>".format(self.user_id, self.voyage_id, self.id)

    @validates('current_chapter')
    def validate_current_chapter(self, key, chapter):
        if chapter not in self.voyage.chapters:
            raise InvalidChapterException('Chapter {} is not available in this voyage'.format(chapter))

        return chapter

    @validates('role')
    def validate_role(self, key, role):
        if role not in ROLES:
            raise InvalidRoleException('Unknown role: {}'.format(role))
        return role
