import datetime
from dress.models.db import *

class TaskLog(db.Model):
    __tablename__ = 'tasklog'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(64), default='unknown')
    custom_data = db.Column(MyJSONType)
    logtime = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, task_name, custom_data):
        self.task_name = task_name
        self.custom_data = custom_data

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
