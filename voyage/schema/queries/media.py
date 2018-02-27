import graphene

from voyage.fields import ConnectionField, Field
from voyage.models import Media


class MediaQuery(object):
    media = Field(
        'Media',
        id=graphene.ID(required=True),
    )
    # I know the plural is media, sue me
    medias = ConnectionField('MediaConnection')

    def resolve_media(root, info, id):
        return Media.query.get(id)

    def resolve_medias(root, info):
        return Media.query
