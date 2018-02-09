from dress.models.db import db

class Setting(db.Model):
    __tablename__ = 'setting'

    name = db.Column(db.String(128), primary_key=True)
    value = db.Column(db.Text)

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

class SettingOrderStartNumber(object):
    NAME = 'order_start_number'
    INIT_VALUE = 10000
    DEFAULT_INTERVAL = 10000

    def __init__(self):
        self.setting_obj = Setting.query.filter_by(name=self.NAME).first()

    def get(self):
        return int(self.setting_obj.value)

    def reset(self, value=INIT_VALUE):
        self.setting_obj.update(value=value)
        return value

    def inc_interval(self, interval=DEFAULT_INTERVAL):
        old_value = self.get()
        new_value= old_value + interval
        self.setting_obj.update(value=str(new_value))
        return new_value
