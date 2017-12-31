from dress import app
from flask_script import Manager, Server

manager = Manager(app)

# use 0.0.0.0 as host IP
manager.add_command('runserver', Server(host="0.0.0.0"))

# test command
@manager.command
def hello():
    print('hello')

if __name__ == "__main__":
    manager.run()
