import os
from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG=config('DEBUG', cast=bool)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Nguyenxuanmai2101@localhost/kinexcs_flask'

class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass

config_dict={
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}