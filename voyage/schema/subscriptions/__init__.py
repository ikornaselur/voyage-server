import graphene

from .voyage import VoyageSubscription


class Subscription(
    graphene.ObjectType,
    VoyageSubscription,
):
    """ Combine all subscriptions into one """
