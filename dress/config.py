# default configration
import os

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = os.environ['APP_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dress.db'

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
