from graphene import ObjectType

from voyage import fields
from voyage.utils.relay import Connection, Node


class Media(ObjectType):
    class Meta:
        interfaces = (Node, )

    id = fields.ID(required=True)

    series = fields.String()
    order = fields.Int()
    name = fields.String()

    type = fields.String()
    chapters = fields.List(fields.String)

    external_url = fields.String()


class MediaConnection(Connection):
    class Meta:
        node = Media
