import random

from voyage.app import create_app
from voyage.extensions import db
from voyage.models import Comment, Media, User, Voyage


def create_users():
    print("[*] Creating users")
    for i in range(5):
        user = User(
            name='Text User {}'.format(i),
            email='TestEmail{}@example.com'.format(i),
            profile_picture='https://robohash.org/{}.png?bgset=bg1&set=set4'.format('user{}'.format(i)),
        )
        db.session.add(user)
    db.session.commit()


def create_medias():
    print("[*] Creating medias")
    for i in range(1, 3):
        media = Media(
            series='Test tv show',
            order=i,
            name='Season #{}'.format(i),
            type='tvshow',
            chapters=list(range(1, 11)),
        )
        db.session.add(media)

    for i in range(1, 4):
        media = Media(
            series='Test books',
            order=i,
            name='Book #{}'.format(i),
            type='book',
            chapters=list(range(1, 50)),
        )
        db.session.add(media)
    db.session.commit()


def create_voyages():
    print("[*] Creating voyages")
    voyage1 = Voyage(
        name='Test voyage 1',
        media=Media.query.first(),
        owner=User.query.first(),
    )

    voyage1.add_member(User.query.offset(1).first())
    voyage1.add_member(User.query.offset(2).first())

    db.session.add(voyage1)
    db.session.commit()

    voyage2 = Voyage(
        name='Test voyage 2',
        media=Media.query.offset(1).first(),
        owner=User.query.offset(2).first(),
    )

    voyage2.add_member(User.query.offset(3).first())
    voyage2.add_member(User.query.offset(4).first())

    db.session.add(voyage2)
    db.session.commit()


def create_comments():
    print("[*] Creating comments")
    voyage = Voyage.query.first()
    for i in range(20):
        comment = Comment(
            user=random.choice(voyage.members),
            voyage=voyage,
            text='This is comment #{}'.format(i),
            chapter=random.choice(voyage.chapters),
        )
        db.session.add(comment)
    db.session.commit()


if __name__ == "__main__":
    with create_app().app_context():
        create_users()
        create_medias()
        create_voyages()
        create_comments()
