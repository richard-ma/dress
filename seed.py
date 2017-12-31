from dress import create_app
from dress.data.models import db, Host, Status

app = create_app()

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

        app.logger.debug('Initial host data importing failed.')

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

        app.logger.debug('Initial status data importing failed.')

def seed_db(app):
    with app.app_context():
        db.drop_all()
        app.logger.debug('Drop all databases')
        db.create_all()
        app.logger.debug('Create all databases')

        seed_status_data(db)
        seed_host_data(db)

if __name__ == '__main__':
    seed_db(app)
