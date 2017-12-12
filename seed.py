from dress import create_app
from dress.data.models import db, Host

def seed_host_data(database):
    pass

def seed_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

        seed_host_data(db)

if __name__ == '__main__':
    flask_app = create_app()
    seed_db(flask_app)
