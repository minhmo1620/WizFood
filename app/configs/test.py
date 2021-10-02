import os
from .base import Config


class TestingConfig(Config):
    TESTING = True
    db_path = os.path.join(os.path.dirname(__file__), 'test.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(db_path)
    SECRET_KEY = 'testing'
