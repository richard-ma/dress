from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Host(db.Model):
    __tablename__ = 'host'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    ip = db.Column(db.String(32))
    port = db.Column(db.Integer)
    domain = db.Column(db.String(32))
    pwd = db.Column(db.String(32))
    db_name = db.Column(db.String(32))
    db_pwd = db.Column(db.String(32))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id', ondelete='CASCADE'))

    status = relationship("Status", back_populates='hosts')

    def __init__(self, ip=None, port=22, domain=None, pwd=None, db_name=None, db_pwd=None, status=None):
        self.ip = ip
        self.port = port
        self.domain = domain
        self.pwd = pwd
        self.db_name = db_name
        self.db_pwd = db_pwd
        self.status = Status.query.all()[0]

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

        return self

    def update(self, ip, port, domain, pwd, db_name, db_pwd, status):
        self.ip = ip
        self.port = port
        self.domain = domain
        self.pwd = pwd
        self.db_name = db_name
        self.db_pwd = db_pwd
        if status != None:
            self.status = Status.query.filter_by(id=status).first()
        else:
            self.status = Status.query.all()[0]

        db.session.commit()

    def name(self):
        return "%s@%s" % (self.domain, self.ip)

    def __repr__(self):
        return '<Host %r>' % (self.name)

class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), unique=True)

    hosts = relationship("Host", back_populates='status')

    def __init__(self, title):
        self.title = title

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

        return self

    def update(self, title):
        self.title = title
        db.session.commit()

    def __repr__(self):
        return '<Status %r>' % (self.title)
