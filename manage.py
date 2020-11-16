import time
from multiprocessing import Process
from threading import Thread

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from conf.dynamic_config import update_access_token

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app("production")
print(app.url_map)

db = SQLAlchemy(app)
manager = Manager(app)

Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


def data_init():
    time.sleep(5)
    from utils.reboot_shell import migrate_init
    migrate_init()  # Migration initialization
    Process(target=update_access_token).start()  # Write access_token value regularly


t = Thread(target=data_init)
t.setDaemon(True)
t.start()

if __name__ == '__main__':
    app.run()
