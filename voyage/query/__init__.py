from graphene import ObjectType

from .media import MediaQuery
from .voyage import VoyageQuery


class Query(
    ObjectType,
    MediaQuery,
    VoyageQuery,
):
    """ Combine all queries into one """
