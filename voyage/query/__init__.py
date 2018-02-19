from graphene import ObjectType

from .media import MediaQuery


class Query(
    ObjectType,
    MediaQuery,
):
    """ Combine all queries into one """
