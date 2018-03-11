from graphene.types import ID

from voyage import events
from voyage.fields import Field


class VoyageSubscription(object):
    voyage_created = Field('Voyage')
    voyage_updated = Field(
        'Voyage',
        voyage_id=ID(name='id', required=True),
    )

    def resolve_voyage_created(root, info):
        return events.voyage.subscribe_created()

    def resolve_voyage_updated(root, info, voyage_id):
        return events.voyage.subscribe_updated(voyage_id=voyage_id)
