from graphene.types import ID, ObjectType, String
from graphene.types.datetime import DateTime

from voyage.fields import Field, List
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


class VoyageConnection(Connection):
    class Meta:
        node = Voyage
