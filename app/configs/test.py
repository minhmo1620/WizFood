import os
from .base import Config


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SECRET_KEY = 'testing'
