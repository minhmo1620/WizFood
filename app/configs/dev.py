import os
from app.configs.base import Config


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'