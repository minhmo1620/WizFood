from ..db import db


class VoteModel(db.Model):
    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    box_id = db.Column(db.Integer, db.ForeignKey("boxes.id"), nullable=False)
    # TODO: store option_id and box_id for future reference
    data = db.Column(db.String, nullable=False)

    def __init__(self, user_id, box_id, data):
        self.user_id = user_id
        self.box_id = box_id
        self.data = data
