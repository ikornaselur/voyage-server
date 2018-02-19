from flask_script import Manager, Shell

from voyage import models
from voyage.app import create_app
from voyage.extensions import db

manager = Manager(create_app)


def _make_context():
    models_dict = {
        key: value
        for key, value
        in models.__dict__.items()
        if key[0].isupper()
    }
    return dict(db=db, **models_dict)


manager.add_command("shell", Shell(make_context=_make_context, use_ipython=True))


if __name__ == "__main__":
    from ipdb import launch_ipdb_on_exception
    with launch_ipdb_on_exception():
        manager.run()
