import os

from app.configs.base import Config


class LocalConfig(Config):
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(db_path)
