import graphene

from .voyage import VoyageMutation


class Mutation(
    graphene.ObjectType,
    VoyageMutation,
):
    """ Combine all mutations into one """
