from flask_login import current_user

from voyage.schema.queries import UserQuery


def test_getting_current_user(graph_client, db_user, client):
    with client.use(db_user):
        user = UserQuery.resolve_current_user('root', 'info')

    assert user == current_user
