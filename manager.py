from dress import app
from dress.data.models import db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)
manager = Manager(app)

# use 0.0.0.0 as host IP
manager.add_command('runserver', Server(host="0.0.0.0"))

# add flask migrate commands
manager.add_command('db', MigrateCommand)

# test command
@manager.command
def hello():
    print('hello')

if __name__ == "__main__":
    print(app)
    manager.run()
