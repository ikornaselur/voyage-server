import pytest

from voyage.exceptions import MutationException
from voyage.schema.mutations.voyage import AddCommentToVoyage, InviteUserToVoyage, RemoveUserFromVoyage


def test_inviting_user_to_voyage(db_voyage, db_user_owner, db_user, client):
    assert db_user not in db_voyage.members

    with client.use(db_user_owner):
        InviteUserToVoyage.mutate('root', 'info', db_voyage.id, db_user.email)

    assert db_user in db_voyage.members


def test_inviting_user_only_allows_owner_to_do_it(db_voyage, db_user_member, db_user, client):
    assert db_user not in db_voyage.members

    with client.use(db_user_member):
        with pytest.raises(MutationException) as exc:
            InviteUserToVoyage.mutate('root', 'info', db_voyage.id, db_user.email)

    assert 'Only voyage owners can invite users' in exc.exconly()
    assert db_user not in db_voyage.members


def test_removing_a_user_from_voyage(db_voyage, db_user_owner, db_user_member, client):
    assert db_user_member in db_voyage.members

    with client.use(db_user_owner):
        RemoveUserFromVoyage.mutate('root', 'info', db_voyage.id, db_user_member.email)

    assert db_user_member not in db_voyage.members


def test_comment_on_chapter(db_voyage, db_user_member, client):
    assert db_user_member in db_voyage.members
    assert len(db_voyage.comments) == 0

    with client.use(db_user_member):
        AddCommentToVoyage.mutate('root', 'info', db_voyage.id, db_voyage.chapters[0], 'A test comment')

    assert len(db_voyage.comments) == 1
    assert db_voyage.comments[0].text == 'A test comment'


def test_comment_on_chapter_fails_if_not_member(db_voyage, db_user, client):
    assert db_user not in db_voyage.members

    with client.use(db_user):
        with pytest.raises(MutationException) as exc:
            AddCommentToVoyage.mutate('root', 'info', db_voyage.id, db_voyage.chapters[0], 'A test comment')

    assert 'Voyage not found' in exc.exconly()


def test_comment_on_chapter_fails_if_users_hasnt_progressed_far_enough(db_voyage, db_user_member, client):
    assert db_user_member in db_voyage.members
    membership = db_user_member.memberships[0]
    assert membership.voyage == db_voyage
    assert membership.current_chapter == db_voyage.chapters[0]

    with client.use(db_user_member):
        with pytest.raises(MutationException) as exc:
            AddCommentToVoyage.mutate('root', 'info', db_voyage.id, db_voyage.chapters[1], 'A test comment')

    assert 'Unable to comment on future chapters' in exc.exconly()
