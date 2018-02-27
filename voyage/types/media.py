import graphene

from voyage.fields import List
from voyage.utils.relay import Connection, Node


class Media(graphene.ObjectType):
    class Meta:
        interfaces = (Node, )

    id = graphene.ID(required=True)

    series = graphene.String()
    order = graphene.Int()
    name = graphene.String()

    type = graphene.String()
    chapters = List(graphene.String)

    external_url = graphene.String()


class MediaConnection(Connection):
    class Meta:
        node = Media
