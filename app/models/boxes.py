from ..db import db


class BoxModel(db.Model):
    __tablename__ = "boxes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    options = db.relationship("OptionModel")

    def __init__(self, user_id, name, description):
        self.owner_id = user_id
        self.name = name
        self.description = description
