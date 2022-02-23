import os
from app.configs.base import Config


class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')