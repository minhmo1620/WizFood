from app import db
from app.models.boxes import BoxModel


def validate_box_id(box_id):
    """
    Validate the box_id. Check if the box exist
    Input:
        - box_id (int) The ID of the box
    """
    box = db.session.query(BoxModel).filter(BoxModel.id == box_id).first()
    return True if (box is not None) else False
