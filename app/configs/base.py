import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    JSON_SORT_KEYS = False
