import graphene

from voyage.fields import Field, List
from voyage.utils.relay import Connection, Node


class Voyage(graphene.ObjectType):
    class Meta:
        interfaces = (Node, )

    id = graphene.ID(required=True)
    name = graphene.String()

    media = Field('Media')

    owner = Field('User')
    members = List('User')


class VoyageConnection(Connection):
    class Meta:
        node = Voyage
