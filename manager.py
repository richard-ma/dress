import unittest
import sys
import os
import csv
from dress import app
from dress.models import *
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)
manager = Manager(app)

# use 0.0.0.0 as host IP
manager.add_command('runserver', Server(host="0.0.0.0"))

# add flask migrate commands
manager.add_command('db', MigrateCommand)

# seed data
def seed_host_data(database):
    example_host1 = Host()
    example_host1.ip = '1.1.1.1'
    example_host1.port = 22
    example_host1.domain = 'example_host1.domain'
    example_host1.pwd = 'example_host1 password'
    example_host1.db_pwd = 'example_host1 database password'
    example_host1.memo = 'example_host1 memo'

    example_host2 = Host()
    example_host2.ip = '2.2.2.2'
    example_host2.port = 22
    example_host2.domain = 'example_host2.domain'
    example_host2.pwd = 'example_host2 password'
    example_host2.db_pwd = 'example_host2 database password'
    example_host2.memo = 'example_host2 memo'

    try:
        database.session.add(example_host1)
        database.session.add(example_host2)

        database.session.commit()

        app.logger.debug('Initial host data imported.')
    except exc.SQLAlchemyError:
        database.session.rollback()

        app.logger.error('Initial host data importing failed.')

def seed_status_data(database):
    prepare_stauts = Status(title=Status.PREPARE)
    business_stauts = Status(title=Status.BUSINESS)
    problem_stauts = Status(title=Status.PROBLEM)
    source_stauts = Status(title=Status.SOURCE)

    try:
        database.session.add(prepare_stauts)
        database.session.add(business_stauts)
        database.session.add(problem_stauts)
        database.session.add(source_stauts)

        database.session.commit()

        app.logger.debug('Initial status data imported.')
    except exc.SQLAlchemyError:
        database.session.rollback()

        app.logger.error('Initial status data importing failed.')

def seed_setting_data(database):
    data = list()
    data.append(Setting(name=SettingOrderStartNumber.NAME, value=SettingOrderStartNumber.INIT_VALUE))

    try:
        for d in data:
            database.session.add(d)

        database.session.commit()

        app.logger.debug('Initial setting data imported.')
    except exc.SQLAlchemyError:
        database.session.rollback()

        app.logger.error('Initial setting data importing failed.')

@manager.command
def importsource():
    csvfilename = 'sourcehost.csv'
    with open(csvfilename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            host = Host()
            host.ip = row[0]
            host.port = row[1]
            host.domain = row[2]
            host.pwd = row[3]
            host.db_pwd = row[4]
            host.memo = row[5]
            host.create()

            host.updateStatus(Status.SOURCE)

@manager.command
def seed():
    db.drop_all()
    app.logger.debug('Drop all databases')
    db.create_all()
    app.logger.debug('Create all databases')

    seed_status_data(db)
    seed_host_data(db)
    seed_setting_data(db)

@manager.command
def hello():
    print('hello')

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        os.environ["DRESS_CONFIGURATION"] = 'testing'
        tests = unittest.TestLoader().discover('tests', pattern='*_tests.py')
        unittest.TextTestRunner(verbosity=1).run(tests)
    else:
        manager.run()
