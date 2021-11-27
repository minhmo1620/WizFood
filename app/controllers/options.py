from flask import Blueprint, jsonify, current_app

from app import db
from app.schemas.options import OptionSchema
from app.models.options import OptionModel
from app.helpers import validate_input, token_required

options_blueprint = Blueprint("options", __name__)

secret_key = current_app.config["SECRET_KEY"]


@options_blueprint.route("/boxes/<int:box_id>/options", methods=["GET"])
def get_options(box_id):
    list_options = db.session.query(OptionModel).filter(OptionModel.box_id == box_id).all()

    return jsonify(OptionSchema(many=True).dump(list_options)), 200


@options_blueprint.route("/boxes/<int:box_id>/options", methods=["POST"])
@token_required
@validate_input(schema=OptionSchema)
def create_new_option(box_id, user_id, data):
    name = data['name']
    description = data['description']

    new_option = OptionModel(name, description, box_id, user_id)
    db.session.add(new_option)
    db.session.commit()

    return new_option.id
