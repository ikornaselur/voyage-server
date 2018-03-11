from graphene.types import ID, String

from voyage.exceptions import QueryException
from voyage.fields import ConnectionField, Field
from voyage.models import Comment, Voyage


class VoyageQuery(object):
    voyage = Field(
        'Voyage',
        voyage_id=ID(required=True),
    )
    voyages = ConnectionField('VoyageConnection')
    comments_for_voyage = ConnectionField(
        'CommentConnection',
        voyage_id=ID(required=True),
        chapter=String(),
    )

    def resolve_voyage(root, info, voyage_id):
        return Voyage.query.get(voyage_id)

    def resolve_voyages(root, info):
        return Voyage.query

    def resolve_comments_for_voyage(root, info, voyage_id, chapter=None):
        voyage = Voyage.query.get(voyage_id)
        if voyage is None:
            raise QueryException('Voyage not found')
        comments = Comment.query.filter(Comment.voyage == voyage)

        if chapter:
            if chapter not in voyage.chapters:
                QueryException('Invalid chapter ({}) for the voyage'.format(chapter))
            comments = comments.filter(Comment.chapter == chapter)

        return comments
