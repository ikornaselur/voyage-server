from flask_login import current_user
from graphene.types import ID, String

from voyage.exceptions import QueryException
from voyage.fields import ConnectionField, Field
from voyage.models import Comment, Membership, Voyage


class VoyageQuery(object):
    voyage = Field(
        'Voyage',
        voyage_id=ID(name='id', required=True),
    )
    voyages = ConnectionField('VoyageConnection')
    comments_for_voyage = ConnectionField(
        'CommentConnection',
        voyage_id=ID(name='id', required=True),
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

        membership = (
            Membership.query
            .filter(
                Membership.voyage == voyage,
                Membership.user == current_user,
            )
        ).first()
        if membership is None:
            raise QueryException('Voyage not found')

        current_chapter_index = voyage.chapters.index(membership.current_chapter)
        allowed_chapters = voyage.chapters[:current_chapter_index + 1]  # Include the current chapter with + 1

        comments = (
            Comment.query
            .filter(
                Comment.voyage == voyage,
                Comment.chapter.in_(allowed_chapters),
            )
        )

        if chapter:
            if chapter not in voyage.chapters:
                QueryException('Invalid chapter ({}) for the voyage'.format(chapter))
            comments = comments.filter(Comment.chapter == chapter)

        return comments
