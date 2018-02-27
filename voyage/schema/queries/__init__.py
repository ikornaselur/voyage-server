import graphene

from .media import MediaQuery
from .user import UserQuery
from .voyage import VoyageQuery


class Query(
    graphene.ObjectType,
    MediaQuery,
    UserQuery,
    VoyageQuery,
):
    """ Combine all queries into one """
