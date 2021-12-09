from flask import Blueprint, jsonify

from app import db
from app.schemas.boxes import BoxSchema
from app.models.boxes import BoxModel
from app.helpers import validate_input, token_required

"""
WizBox is one main feature of WizFood, which aims to create a room/box for everyone to gather food choices in a 
group hanging out event.
"""
boxes_blueprint = Blueprint("boxes", __name__)


@boxes_blueprint.route("/boxes", methods=["GET"])
@token_required
def get_all_boxes(user_id):
    """
    :param user_id:
    :return: All boxes created by user_id
    """
    list_boxes = db.session.query(BoxModel).filter(BoxModel.owner_id == user_id).all()

    return jsonify(BoxSchema(many=True).dump(list_boxes)), 200


@boxes_blueprint.route("/boxes/<int:box_id>", methods=["GET"])
@token_required
def get_box(user_id, box_id):
    """
    :param box_id: ID of the box
    :param user_id: Who is querying?
    :return: One box matched with box_id
    """
    box = db.session.query(BoxModel).filter(BoxModel.id == box_id).first()
    if box is None:
        return jsonify({'message': 'Cannot find the wizbox'}), 404

    return jsonify(BoxSchema().dump(box)), 200


@boxes_blueprint.route("/boxes", methods=["POST"])
@token_required
@validate_input(schema=BoxSchema)
def create_new_box(user_id, data):
    """
    :param user_id: who is creating this box
    :param data:
        - name: name of the box
        - description: description of the event
    :return: A new box created by user_id
    """
    name = data['name']
    description = data['description']

    # TODO: status of the box (Open/closed)

    new_box = BoxModel(user_id, name, description)
    db.session.add(new_box)
    db.session.commit()

    return jsonify(BoxSchema().dump(new_box)), 201
