from ..db import db


class FoodModel(db.Model):
    __tablename__ = "foods"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    data =  db.Column(db.String(300), nullable=False)

    def __init__(self, user_id, name, data):
        self.user_id = user_id
        self.name = name
        self.data = data
