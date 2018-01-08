from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Host(db.Model):
    __tablename__ = 'host'

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(32))
    port = db.Column(db.Integer)
    domain = db.Column(db.String(32))
    pwd = db.Column(db.String(32))
    db_pwd = db.Column(db.String(32))
    memo = db.Column(db.String(32))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id', ondelete='CASCADE'))

    status = relationship("Status", back_populates='hosts')

    def __init__(self, ip=None, port=22, domain=None, pwd=None, db_pwd=None, memo=None, status=None):
        self.ip = ip
        self.port = port
        self.domain = domain
        self.pwd = pwd
        self.db_pwd = db_pwd
        self.memo = memo
        self.status = Status.query.all()[0]

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.SQLAlchemyError:
            database.session.rollback()

            app.logger.error(self)

        return self

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except exc.SQLAlchemyError:
            database.session.rollback()

            app.logger.error(self)

        return self

    def update(self, ip, port, domain, pwd, db_pwd, memo, status):
        self.ip = ip
        self.port = port
        self.domain = domain
        self.pwd = pwd
        self.db_pwd = db_pwd
        self.memo = memo
        if status != None:
            self.status = Status.query.filter_by(id=status).first()
        else:
            self.status = Status.query.all()[0]

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            database.session.rollback()

            app.logger.error(self)

        return self

    def updateStatus(self, status):
        self.status = Status.query.filter_by(title=status).first()

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            database.session.rollback()

            app.logger.error(self)

        return self

    def name(self):
        return "%s@%s" % (self.domain, self.ip)

    def __repr__(self):
        return '<Host %r>' % (self.name)

class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), unique=True)

    hosts = relationship("Host", back_populates='status')

    PREPARE = 'prepare'
    BUSINESS = 'business'
    PROBLEM = 'problem'
    SOURCE = 'source'

    def __init__(self, title):
        self.title = title

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.SQLAlchemyError:
            database.session.rollback()

            app.logger.error(self)

        return self

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except exc.SQLAlchemyError:
            database.session.rollback()

            app.logger.error(self)

        return self

    def update(self, title):
        self.title = title
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            database.session.rollback()

            app.logger.error(self)

    def __repr__(self):
        return '<Status %r>' % (self.title)

class Setting(db.Model):
    __tablename__ = 'setting'

    name = db.Column(db.String(128), primary_key=True)
    value = db.Column(db.Text)

    ORDER_START_NUMBER_NAME = 'start_order_number'
    ORDER_START_NUMBER_VALUE = '10000'

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.SQLAlchemyError:
            database.session.rollback()

            app.logger.error(self)

        return self

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except exc.SQLAlchemyError:
            database.session.rollback()

            app.logger.error(self)

        return self

    def update(self, value):
        self.value = value
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            database.session.rollback()

            app.logger.error(self)

    def __repr__(self):
        return '<Setting %r=%r>' % (self.name, self.value)
