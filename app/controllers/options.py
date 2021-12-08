from flask import Blueprint, jsonify

from app import db
from app.schemas.options import OptionSchema
from app.models.options import OptionModel
from app.helpers import validate_input, token_required
from app.controllers.helpers import validate_box_id

"""
In each box, user can add their food recommendation as an option for everyone to vote later
"""
options_blueprint = Blueprint("options", __name__)


@options_blueprint.route("/boxes/<int:box_id>/options", methods=["GET"])
def get_options(box_id):
    """
    Get all options of one box based on box_id
    """
    if not validate_box_id(box_id):
        return jsonify({'message': 'Cannot find the wizbox'}), 404

    list_options = db.session.query(OptionModel).filter(OptionModel.box_id == box_id).all()

    return jsonify(OptionSchema(many=True).dump(list_options)), 200


@options_blueprint.route("/boxes/<int:box_id>/options", methods=["POST"])
@token_required
@validate_input(schema=OptionSchema)
def create_new_option(box_id, user_id, data):
    """
    Create new option in one specific box
    """
    name = data['name']
    description = data['description']

    if not validate_box_id(box_id):
        return jsonify({'message': 'Cannot find the wizbox'}), 404

    new_option = OptionModel(name, description, box_id, user_id)
    db.session.add(new_option)
    db.session.commit()

    return jsonify(OptionSchema().dump(new_option)), 201
