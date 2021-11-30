import json

from flask import Blueprint, jsonify

from app import db
from app.schemas.boxes import BoxSchema
from app.schemas.votes import VoteSchema
from app.models.boxes import BoxModel
from app.models.options import OptionModel
from app.models.votes import VoteModel
from app.helpers import validate_input, token_required

from controllers.helpers import validate_box_id

boxes_blueprint = Blueprint("boxes", __name__)


@boxes_blueprint.route("/boxes", methods=["GET"])
@token_required
def get_all_boxes(user_id):
    list_boxes = db.session.query(BoxModel).filter(BoxModel.user_id == user_id).all()

    return jsonify(BoxSchema(many=True).dump(list_boxes)), 200


@boxes_blueprint.route("/boxes", methods=["POST"])
@token_required
@validate_input(schema=BoxSchema)
def create_new_box(user_id, data):
    name = data['name']
    description = data['description']

    # TODO: status of the box (Open/closed)

    new_box = BoxModel(user_id, name, description)
    db.session.add(new_box)
    db.session.commit()

    return jsonify(BoxSchema().dump(new_box)), 201


@boxes_blueprint.route("/boxes/<int:box_id>/vote", methods=["POST"])
@token_required
@validate_input(schema=VoteSchema)
def vote_options(user_id, box_id, data):
    data = data['votes']

    # Validate the box_id
    if not validate_box_id(box_id):
        return jsonify({'message': 'Cannot find the wizbox'}), 404

    # Query all options of one box
    all_options = db.session.query(OptionModel).filter(OptionModel.box_id == box_id).all()

    # Validate the option in data
    option_id_list = [str(option.id) for option in all_options]
    if option_id_list != list(data.keys()):
        return jsonify({"message": "Please vote all available options"}), 400

    for option in all_options:
        option_id = str(option.id)
        # Update the vote value
        vote_value = data[option_id]
        option_vote_value = json.loads(option.vote)
        option_vote_value[vote_value] += 1
        option.vote = json.dumps(option_vote_value)
    db.session.commit()

    new_vote = VoteModel(user_id, json.dumps(data))
    db.session.add(new_vote)
    db.session.commit()
    return jsonify({"message": "Voted successfully"}), 201
