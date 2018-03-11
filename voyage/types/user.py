from graphene.types import ID, ObjectType, String
from graphene.types.datetime import DateTime


class User(ObjectType):
    id = ID()
    created = DateTime()
    modified = DateTime()

    name = String()
    email = String()
    profile_picture = String()
