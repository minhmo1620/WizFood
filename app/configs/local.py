import os

from app.configs.base import Config


class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
