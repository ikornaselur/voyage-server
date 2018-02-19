from flask_script import Manager, Shell

from voyage.app import create_app

manager = Manager(create_app)


def _make_context():
    pass


manager.add_command("shell", Shell(make_context=_make_context, use_ipython=True))


if __name__ == "__main__":
    from ipdb import launch_ipdb_on_exception
    with launch_ipdb_on_exception():
        manager.run()
