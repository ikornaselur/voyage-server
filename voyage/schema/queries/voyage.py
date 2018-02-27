import graphene

from voyage.fields import ConnectionField, Field
from voyage.models import Voyage


class VoyageQuery(object):
    voyage = Field(
        'Voyage',
        id=graphene.ID(required=True),
    )
    voyages = ConnectionField('VoyageConnection')

    def resolve_voyage(root, info, id):
        return Voyage.query.get(id)

    def resolve_voyages(root, info):
        return Voyage.query
