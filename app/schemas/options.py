import json

from marshmallow import fields, validate, post_dump

from .bases import Base


class OptionSchema(Base):
    name = fields.Str(required=True, validate=validate.Length(max=100, min=1))
    description = fields.Str(required=True, validate=validate.Length(max=200, min=1))
    id = fields.Int(required=False)
    vote = fields.Str(required=False)

    @post_dump
    def load_vote(self, data, **kwargs):
        data['vote'] = json.loads(data['vote'])
        return data
