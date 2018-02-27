from flask_login import current_user

from voyage.fields import Field


class UserQuery(object):
    current_user = Field('User')

    def resolve_current_user(root, info):
        return current_user
