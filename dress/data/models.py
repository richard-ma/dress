from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    ip = db.Column(db.String(32))
    port = db.Column(db.Integer)
    domain = db.Column(db.String(32))
    pwd = db.Column(db.String(32))
    db_name = db.Column(db.String(32))
    db_pwd = db.Column(db.String(32))

    def __init__(self, name, ip, port, domain, pwd, db_name, db_pwd):
        self.name = name
        self.ip = ip
        self.port = port
        self.domain = domain
        self.pwd = pwd
        self.db_name = db_name
        self.db_pwd = db_pwd

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, name, ip, port, domain, pwd, db_name, db_pwd):
        self.name = name
        self.ip = ip
        self.port = port
        self.domain = domain
        self.pwd = pwd
        self.db_name = db_name
        self.db_pwd = db_pwd
        db.session.commit()

    def __repr__(self):
        return '<Host %r>' % (self.name)
