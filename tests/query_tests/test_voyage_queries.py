import pytest

from voyage.exceptions import QueryException
from voyage.models import Comment, Membership, Voyage
from voyage.schema.queries import VoyageQuery


def test_getting_all_voyages(db_voyage):
    voyages = VoyageQuery.resolve_voyages('root', 'info').all()
    assert voyages == [db_voyage]


def test_getting_single_voyage(db_voyage):
    voyage = VoyageQuery.resolve_voyage('root', 'info', db_voyage.id)
    assert voyage == db_voyage


def test_getting_comments_for_chapter_user_has_access_to(db_session, db_voyage, db_user_member, client):
    assert db_user_member in db_voyage.members

    comment = Comment(
        voyage=db_voyage,
        user=db_user_member,
        text='Test comment',
        chapter=db_voyage.chapters[0],
    )
    db_session.add(comment)

    other_voyage = Voyage(name='Other voyage', media=db_voyage.media, owner=db_user_member)
    db_session.add(other_voyage)

    other_comment = Comment(
        voyage=other_voyage,
        user=db_user_member,
        text='Different comment',
        chapter=other_voyage.chapters[0],
    )
    db_session.add(other_comment)

    db_session.commit()

    with client.use(db_user_member):
        comments = VoyageQuery.resolve_comments_for_voyage('root', 'info', db_voyage.id).all()
    assert len(comments) == 1
    assert comments[0] == comment


def test_getting_comments_raises_if_user_not_member_of_voyage(db_voyage, db_user, client):
    assert db_user not in db_voyage.members

    with client.use(db_user):
        with pytest.raises(QueryException) as exc:
            VoyageQuery.resolve_comments_for_voyage('root', 'info', db_voyage.id)

    assert 'Voyage not found' in exc.exconly()


def test_getting_comments_doesnt_show_user_comments_in_future_chapters(
        db_session, db_voyage, db_user_owner, db_user_member, client):
    comment = Comment(
        voyage=db_voyage,
        user=db_user_member,
        text='Test comment, on future chapter',
        chapter=db_voyage.chapters[1],
    )
    db_session.add(comment)

    db_session.commit()

    membership = (
        Membership.query
        .filter(
            Membership.voyage == db_voyage,
            Membership.user == db_user_owner,
        )
    ).first()
    assert membership.current_chapter == db_voyage.chapters[0]

    with client.use(db_user_owner):
        comments = VoyageQuery.resolve_comments_for_voyage('root', 'info', db_voyage.id).all()
    assert len(comments) == 0

    membership.current_chapter = db_voyage.chapters[1]  # The chapter the comment was on
    db_session.commit()

    with client.use(db_user_owner):
        comments = VoyageQuery.resolve_comments_for_voyage('root', 'info', db_voyage.id).all()
    assert len(comments) == 1
