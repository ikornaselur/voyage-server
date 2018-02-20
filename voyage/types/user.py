from graphene import ObjectType

from voyage import fields


class User(ObjectType):
    id = fields.ID()
    name = fields.String()
    email = fields.String()
    profile_picture = fields.String()
