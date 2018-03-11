from graphene.types import ID, ObjectType, String
from graphene.types.datetime import DateTime
from graphene.types.generic import GenericScalar
from sqlalchemy import func

from voyage.extensions import db
from voyage.fields import Field, List
from voyage.models import Comment
from voyage.utils.relay import Connection, Node


class Voyage(ObjectType):
    class Meta:
        interfaces = (Node, )

    id = ID(required=True)
    created = DateTime()
    modified = DateTime()

    name = String()

    media = Field('Media')

    owner = Field('User')
    members = List('User')

    comment_counts = GenericScalar()

    def resolve_comment_counts(root, info):
        # Initialize a dictionary with 0 comment count per chapter
        base_dict = dict.fromkeys(root.chapters, 0)

        counts = (
            db.session
            .query(Comment.chapter, func.count(Comment.id))
            .filter(Comment.voyage == root)
            .group_by(Comment.chapter)
        ).all()

        base_dict.update(dict(counts))
        return base_dict


class VoyageConnection(Connection):
    class Meta:
        node = Voyage
