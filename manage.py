from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from flaskr.init import app
from models import db, set_up

set_up(app)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()