from graphene.types import ID

from voyage.fields import ConnectionField, Field
from voyage.models import Media


class MediaQuery(object):
    media = Field(
        'Media',
        media_id=ID(name='id', required=True),
    )
    # I know the plural is media, sue me
    medias = ConnectionField('MediaConnection')

    def resolve_media(root, info, media_id):
        return Media.query.get(media_id)

    def resolve_medias(root, info):
        return Media.query
