from voyage import events, fields


class VoyageSubscription(object):
    voyage_created = fields.Field('Voyage')
    voyage_updated = fields.Field('Voyage',
        id=fields.ID(required=True),
    )

    def resolve_voyage_created(root, info):
        return events.voyage.subscribe_created()

    def resolve_voyage(root, info, id):
        return events.voyage.subscribe_updated(voyage_id=id)
