from voyage.extensions import db
from voyage.utils import UUIDString, uuid4_str


class Voyage(db.Model):
    __tablename__ = 'voyage'

    id = db.Column(UUIDString, primary_key=True, default=uuid4_str)
    name = db.Column(db.String, nullable=False)

    media_id = db.Column(UUIDString, db.ForeignKey('media.id'), nullable=False)
    media = db.relationship('Media')

    def __init__(self, name, media, owner):
        from voyage.models import Membership

        self.name = name
        self.media = media

        self.memberships = [
            Membership(
                user=owner,
                voyage=self,
                role='owner',
            ),
        ]

    def __repr__(self):
        return "<Voyage: {} ({})>".format(self.name, self.id)

    @property
    def members(self):
        from voyage.models import Membership, User

        return (
            User.query
            .join(Membership)
            .filter(
                Membership.voyage == self,
            )
        ).all()

    @property
    def owner(self):
        from voyage.models import Membership, User

        return (
            User.query
            .join(Membership)
            .filter(
                Membership.voyage == self,
                Membership.role == 'owner',
            )
        ).first()

    @property
    def chapters(self):
        return self.media.chapters

    def add_member(self, user):
        from voyage.models import Membership

        exists = (
            Membership.query
            .filter(
                Membership.user == user,
                Membership.voyage == self,
            )
        ).first()

        if exists:
            exists.active = True
        else:
            self.memberships.append(
                Membership(
                    user=user,
                    voyage=self,
                )
            )

    def remove_member(self, user):
        from voyage.models import Membership

        exists = (
            Membership.query
            .filter(
                Membership.user == user,
                Membership.voyage == self,
            )
        ).first()

        if exists:
            exists.active = False
