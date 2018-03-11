from graphene.types import ID, Int, ObjectType, String
from graphene.types.datetime import DateTime

from voyage.fields import List
from voyage.utils.relay import Connection, Node


class Media(ObjectType):
    class Meta:
        interfaces = (Node, )

    id = ID(required=True)
    created = DateTime()
    modified = DateTime()

    series = String()
    order = Int()
    name = String()

    type = String()
    chapters = List(String)

    external_url = String()


class MediaConnection(Connection):
    class Meta:
        node = Media
