from ..db import db


class KnowledgeBaseModel(db.Model):
    __tablename__ = "knowledgebases"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    kb = db.Column(db.Text(4294000000), nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id
        self.kb = ""
