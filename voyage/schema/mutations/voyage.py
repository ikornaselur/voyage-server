from flask_login import current_user
from graphene.types import ID, Mutation, String

from voyage import events
from voyage.exceptions import MutationException
from voyage.extensions import db
from voyage.fields import Field
from voyage.models import Media, User, Voyage


class CreateVoyage(Mutation):
    class Arguments:
        media_id = ID(required=True, description='ID of the media that this voyage is for')
        name = String(required=True, description='Name of the voyage')

    voyage = Field('Voyage')

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

        events.voyage.created(voyage)

        return CreateVoyage(voyage=voyage)


class InviteUserToVoyage(Mutation):
    class Arguments:
        voyage_id = ID(required=True, description='ID of the voyage to invite to')
        email = String(required=True, description='Email of the user to invite')

    voyage = Field('Voyage')

    def mutate(root, info, voyage_id, email):
        voyage = Voyage.query.get(voyage_id)

        if voyage is None:
            raise MutationException('Voyage not found')

        if voyage.owner != current_user:
            raise MutationException('Only voyage owners can invite users')

        user = User.query.filter(User.email == email).first()

        if user is None:
            # TODO: Invite the user
            raise MutationException('User not signed up')

        if user in voyage.members:
            raise MutationException('User already a part of the mutation')

        voyage.add_member(user)
        db.session.commit()

        events.voyage.updated(voyage)

        return InviteUserToVoyage(voyage=voyage)


class RemoveUserFromVoyage(Mutation):
    class Arguments:
        voyage_id = ID(required=True, description='ID of the voyage to remove from')
        email = String(required=True, description='Email of the user to remove')

    voyage = Field('Voyage')

    def mutate(root, info, voyage_id, email):
        voyage = Voyage.query.get(voyage_id)

        if voyage is None:
            raise MutationException('Voyage not found')

        if voyage.owner != current_user:
            raise MutationException('Only voyage owners can remove users')

        user = User.query.filter(User.email == email).first()

        if user is None:
            # TODO: Invite the user
            raise MutationException('User not signed up')

        if user not in voyage.members:
            raise MutationException("User isn't a part of the voyage")

        if user is voyage.owner:
            raise MutationException("Owners can't be removed from their voyage")

        voyage.remove_member(user)
        db.session.commit()

        events.voyage.updated(voyage)

        return RemoveUserFromVoyage(voyage=voyage)


class VoyageMutation(object):
    create_voyage = CreateVoyage.Field()
    invite_user_to_voyage = InviteUserToVoyage.Field()
    remove_user_from_voyage = RemoveUserFromVoyage.Field()
