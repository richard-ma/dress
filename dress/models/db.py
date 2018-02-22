from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# magic type for json to text
# https://www.michaelcho.me/article/json-field-type-in-sqlalchemy-flask-python
import json
from sqlalchemy.types import TypeDecorator

class MyJSONType(TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)
