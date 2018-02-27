from graphene import ObjectType

from .voyage import VoyageSubscription


class Subscription(
    ObjectType,
    VoyageSubscription,
):
    """ Combine all subscriptions into one """
