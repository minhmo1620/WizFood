import json

from ..db import db


class ConversationModel(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    answers = db.Column(db.String(100))
    ended = db.Column(db.Boolean)

    def __init__(self, user_id):
        self.user_id = user_id
        self.answers = json.dumps([])
        self.ended = 0
