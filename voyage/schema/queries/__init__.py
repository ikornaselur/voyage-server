from graphene import ObjectType

from .media import MediaQuery
from .user import UserQuery
from .voyage import VoyageQuery


class Query(
    ObjectType,
    MediaQuery,
    UserQuery,
    VoyageQuery,
):
    """ Combine all queries into one """
