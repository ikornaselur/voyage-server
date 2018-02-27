from voyage import fields
from voyage.subjects import voyage_subject


class VoyageSubscription(object):
    voyage = fields.Field(
        'Voyage',
        id=fields.ID(required=True),
    )

    def resolve_voyage(root, info, id):
        return voyage_subject.subscribe_updated(voyage_id=id)
