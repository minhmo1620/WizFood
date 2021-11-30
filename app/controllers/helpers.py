from app import db
from app.models.boxes import BoxModel


def validate_box_id(box_id):
    box = db.session.query(BoxModel).filter(BoxModel.id == box_id).first()
    return True if (box is not None) else False
