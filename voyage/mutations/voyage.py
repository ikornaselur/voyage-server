from graphene import Mutation

from flask_login import current_user

from voyage import fields
from voyage.exceptions import MutationException
from voyage.extensions import db
from voyage.models import Media, Voyage


class CreateVoyage(Mutation):
    class Arguments:
        media_id = fields.ID(required=True, description='ID of the media that this voyage is for')
        name = fields.String(required=True, description='Name of the voyage')

    voyage = fields.Field('Voyage')

    def mutate(root, info, media_id, name):
        media = Media.query.get(media_id)
        if media is None:
            raise MutationException('Media not found')

        voyage = Voyage(
            name=name,
            media=media,
            owner=current_user,
            members=[current_user],
        )

        db.session.add(voyage)
        db.session.commit()

        return CreateVoyage(voyage=voyage)


class VoyageMutation(object):
    create_voyage = CreateVoyage.Field()
