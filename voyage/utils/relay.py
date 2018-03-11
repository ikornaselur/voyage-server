from graphene import relay
from graphene.types import Int


class Node(relay.Node):
    class Meta:
        name = 'Node'

    @staticmethod
    def to_global_id(type, id):
        return id

    @staticmethod
    def get_node_from_global_id(id, context, info, only_type=None):
        raise NotImplemented


class Connection(relay.Connection):
    class Meta:
        abstract = True

    count = Int()
