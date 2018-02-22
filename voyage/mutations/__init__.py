from graphene import ObjectType

from .voyage import VoyageMutation


class Mutation(
    ObjectType,
    VoyageMutation,
):
    """ Combine all mutations into one """
