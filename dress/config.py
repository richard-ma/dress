# default configration
import os
import logging

class BaseConfig(object):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'sqlite://' # use memory for sqlite
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'example secret key'

    LOGGING_LOCATION = 'dress.log'
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    #CACHE_TYPE = 'simple'

    #COMPRESS_MIMETYPES = ['text/html', 'text/xml', 'application/json']
    #COMPRESS_LEVEL = 6
    #COMPRESS_MIN_SIZE = 500

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dress_development.db'

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dress_production.db'

class TestingConfig(BaseConfig):
    TESTING = True

config = {
        "development": "dress.config.DevelopmentConfig",
        "testing": "dress.config.TestingConfig",
        "default": "dress.config.BaseConfig",
}

def configure_app(app):
    config_name = os.getenv('DRESS_CONFIGURATION', 'development')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)

    #logging
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
