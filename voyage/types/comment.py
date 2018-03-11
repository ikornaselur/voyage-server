from graphene.types import ID, ObjectType, String
from graphene.types.datetime import DateTime

from voyage.fields import Field
from voyage.utils.relay import Connection, Node


class Comment(ObjectType):
    class Meta:
        interfaces = (Node, )

    id = ID(required=True)
    created = DateTime()
    modified = DateTime()

    user = Field('User')
    voyage = Field('Voyage')

    text = String()
    chapter = String()


class CommentConnection(Connection):
    class Meta:
        node = Comment
