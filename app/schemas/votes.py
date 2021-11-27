from marshmallow import fields, validate

from .bases import Base


class VoteSchema(Base):
    votes = fields.Dict(key=fields.Integer(), values=fields.Integer(validate=validate.Range(min=0, max=2)))

