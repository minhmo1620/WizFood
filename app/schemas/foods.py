import json

from marshmallow import fields, validate, post_dump

from .bases import Base


class FoodSchema(Base):
    def __init__(self):
        pass