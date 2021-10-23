from marshmallow import fields, validate

from .bases import Base


class ConversationSchema(Base):
    username = fields.Str(required=True,
                          validate=validate.Length(max=80, min=1))


class UpdateConversationSchema(Base):
    username = fields.Str(required=True,
                          validate=validate.Length(max=80, min=1))
    answer = fields.Str(required=True,
                          validate=validate.Length(max=80, min=1))