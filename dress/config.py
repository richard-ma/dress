# default configration
import os

class BaseConfig(object):
    DEBUG = False
    if 'APP_SECRET_KEY' in os.environ:
        SECRET_KEY = os.environ['APP_SECRET_KEY']
    else:
        SECRET_KEY = 'example secret key'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///dress.db'

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
