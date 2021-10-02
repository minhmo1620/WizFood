from marshmallow import fields, validate

from .bases import Base


class UserSchema(Base):
    username = fields.Str(required=True,
                          validate=validate.Length(max=80, min=1))
    password = fields.Str(required=True,
                          validate=validate.Length(max=100, min=1))
