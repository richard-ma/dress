from dress import create_app
from dress.data.models import db, Host, Status

def seed_host_data(database):
    example_host1 = Host('example1')
    example_host2 = Host('example2')
    try:
        database.session.add(example_host1)
        database.session.add(example_host2)

        database.session.commit()
    except exc.SQLAlchemyError:
        database.session.rollback()

def seed_status_data(database):
    prepare_stauts = Status(title='Prepare')
    business_stauts = Status(title='Business')
    problem_stauts = Status(title='Problem')

    try:
        database.session.add(prepare_stauts)
        database.session.add(business_stauts)
        database.session.add(problem_stauts)

        database.session.commit()
    except exc.SQLAlchemyError:
        database.session.rollback()

def seed_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

        seed_status_data(db)
        seed_host_data(db)

if __name__ == '__main__':
    flask_app = create_app()
    seed_db(flask_app)
