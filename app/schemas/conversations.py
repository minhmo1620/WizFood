from marshmallow import fields, validate

from .bases import Base


class UpdateConversationSchema(Base):
    answer = fields.Str(required=True,
                          validate=validate.Length(max=80, min=1))