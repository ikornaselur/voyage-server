import graphene

from voyage.exceptions import QueryException
from voyage.fields import ConnectionField, Field
from voyage.models import Voyage


class VoyageQuery(object):
    voyage = Field(
        'Voyage',
        voyage_id=graphene.ID(required=True),
    )
    voyages = ConnectionField('VoyageConnection')
    comments_for_voyage = ConnectionField(
        'CommentConnection',
        voyage_id=graphene.ID(required=True),
    )

    def resolve_voyage(root, info, voyage_id):
        return Voyage.query.get(voyage_id)

    def resolve_voyages(root, info):
        return Voyage.query

    def resolve_comments_for_voyage(root, info, voyage_id):
        voyage = Voyage.query.get(voyage_id)
        if voyage is None:
            raise QueryException('Voyage not found')
        return voyage.comments
