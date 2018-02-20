from flask_login import current_user

from voyage import fields


class UserQuery(object):
    current_user = fields.Field('User')

    def resolve_current_user(root, info):
        return current_user
