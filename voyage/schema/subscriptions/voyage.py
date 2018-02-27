from rx.subjects import Subject

from voyage import fields

voyage_subject = Subject()


class VoyageSubscription(object):
    voyage = fields.Field(
        'Voyage',
        id=fields.ID(required=True),
    )

    def resolve_voyage(root, info, id):
        return voyage_subject.filter(lambda voyage: voyage.id == id)
