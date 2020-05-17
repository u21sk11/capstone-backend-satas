from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from flaskr.init import create_app
from models import db, set_up

app = create_app()
set_up(app)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()