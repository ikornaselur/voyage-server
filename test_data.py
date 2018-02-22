from itertools import chain

from voyage.app import create_app
from voyage.extensions import db
from voyage.models import Media, Voyage

if __name__ == "__main__":
    with create_app().app_context():
        stormlight2 = Media(
            series='Stormlight Archive',
            order=2,
            name='Words of Radiance',
            type='book',
            external_url='https://www.goodreads.com/book/show/17332218-words-of-radiance',
            chapters=list(chain(
                ['Prologue'],
                [str(x) for x in range(1, 13)],
                ['I-1', 'I-2', 'I-3', 'I-4'],
                [str(x) for x in range(13, 35)],
                ['I-5', 'I-6', 'I-7', 'I-8'],
                [str(x) for x in range(35, 59)],
                ['I-9', 'I-10', 'I-11'],
                [str(x) for x in range(59, 76)],
                ['I-12', 'I-13', 'I-14'],
                [str(x) for x in range(76, 90)],
                ['Epilogue'],
            )),
        )
        db.session.add(stormlight2)
        db.session.commit()
