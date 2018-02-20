from voyage import fields
from voyage.models import Media


class MediaQuery(object):
    media = fields.Field(
        'Media',
        id=fields.ID(required=True),
    )
    # I know the plural is media, sue me
    medias = fields.ConnectionField('MediaConnection')

    def resolve_media(root, info, id):
        return Media.query.get(id)

    def resolve_medias(root, info):
        return Media.query
