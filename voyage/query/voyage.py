from voyage import fields
from voyage.models import Voyage


class VoyageQuery(object):
    voyage = fields.Field(
        'Voyage',
        id=fields.ID(required=True),
    )
    voyages = fields.ConnectionField('VoyageConnection')

    def resolve_voyage(root, info, id):
        return Voyage.query.get(id)

    def resolve_voyages(root, info):
        return Voyage.query
