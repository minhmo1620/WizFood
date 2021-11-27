import json

from ..db import db


class OptionModel(db.Model):
    __tablename__ = "options"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    box_id = db.Column(db.Integer, db.ForeignKey("boxes.id"), nullable=False)

    def __init__(self, name, description, box_id, user_id):
        self.name = name
        self.description = description
        self.box_id = box_id
        self.user_id = user_id
        self.vote = json.dumps([0, 0, 0])
