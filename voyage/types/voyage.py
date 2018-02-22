from graphene import ObjectType

from voyage import fields
from voyage.utils.relay import Connection, Node


class Voyage(ObjectType):
    class Meta:
        interfaces = (Node, )

    id = fields.ID(required=True)
    name = fields.String()

    media = fields.Field('Media')

    owner = fields.Field('User')
    members = fields.List('User')


class VoyageConnection(Connection):
    class Meta:
        node = Voyage
