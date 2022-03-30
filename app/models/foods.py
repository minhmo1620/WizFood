import json

from ..db import db


class FoodModel(db.Model):
    __tablename__ = "foods"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    metadata =  db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, metadata):
        self.user_id = user_id
        self.metadata = metadata
