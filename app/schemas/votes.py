import json

from marshmallow import fields, validate, post_dump

from .bases import Base


class VoteSchema(Base):
    votes = fields.Dict(keys=fields.Integer(), values=fields.Integer(validate=validate.Range(min=0, max=2)))


class VoteDataSchema(Base):
    id = fields.Int(required=False)
    data = fields.Str(required=False)

    @post_dump
    def load_vote(self, data, **kwargs):
        if 'data' in data:
            data['data'] = json.loads(data['data'])
            return data
        return data
