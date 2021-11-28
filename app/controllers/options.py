from flask import Blueprint, jsonify

from app import db
from app.schemas.options import OptionSchema
from app.models.options import OptionModel
from app.models.boxes import BoxModel
from app.helpers import validate_input, token_required

options_blueprint = Blueprint("options", __name__)


@options_blueprint.route("/boxes/<int:box_id>/options", methods=["GET"])
def get_options(box_id):
    box = db.session.query(BoxModel).filter(BoxModel.id == box_id).first()
    if box is None:
        return jsonify({'message': 'Cannot find the wizbox'}), 404

    list_options = db.session.query(OptionModel).filter(OptionModel.box_id == box_id).all()

    return jsonify(OptionSchema(many=True).dump(list_options)), 200


@options_blueprint.route("/boxes/<int:box_id>/options", methods=["POST"])
@token_required
@validate_input(schema=OptionSchema)
def create_new_option(box_id, user_id, data):
    name = data['name']
    description = data['description']

    box = db.session.query(BoxModel).filter(BoxModel.id == box_id).first()
    if box is None:
        return jsonify({'message': 'Cannot find the wizbox'}), 404

    new_option = OptionModel(name, description, box_id, user_id)
    db.session.add(new_option)
    db.session.commit()

    return jsonify(OptionSchema().dump(new_option)), 200
