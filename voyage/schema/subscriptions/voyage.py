import graphene

from voyage import events
from voyage.fields import Field


class VoyageSubscription(object):
    voyage_created = Field('Voyage')
    voyage_updated = Field('Voyage',
        id=graphene.ID(required=True),
    )

    def resolve_voyage_created(root, info):
        return events.voyage.subscribe_created()

    def resolve_voyage_updated(root, info, id):
        return events.voyage.subscribe_updated(voyage_id=id)
