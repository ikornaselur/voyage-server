from voyage import fields
from voyage.models import Media


class MediaQuery(object):
    media = fields.ConnectionField('MediaConnection')

    def resolve_media(root, info):
        return Media.query
