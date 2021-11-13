import json

from ..db import db


class ConversationModel(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    answers = db.Column(db.String(100))
    ended = db.Column(db.Boolean)

    def __init__(self, username):
        self.username = username
        self.answers = json.dumps([])
        self.ended = 0
