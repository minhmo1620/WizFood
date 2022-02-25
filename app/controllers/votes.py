import json
from flask import jsonify, Blueprint, request
from app import db

from app.controllers.helpers import validate_box_id
from app.helpers import validate_input, token_required
from app.models.options import OptionModel
from app.models.votes import VoteModel
from app.schemas.votes import VoteSchema, VoteDateSchema

votes_blueprint = Blueprint("votes", __name__)


@votes_blueprint.route("/boxes/<int:box_id>/vote", methods=["GET"])
@token_required
def get_vote_data(user_id, box_id):
    # Validate the box_id
    if not validate_box_id(box_id):
        return jsonify({'message': 'Cannot find the wizbox'}), 404

    vote = db.session.query(VoteModel).filter(VoteModel.box_id == box_id).filter(VoteModel.user_id == user_id).first()
    if vote:
        return jsonify(VoteDateSchema().dump(vote)), 200

    return jsonify({}), 200


@votes_blueprint.route("/boxes/<int:box_id>/vote", methods=["POST", "PUT"])
@token_required
@validate_input(schema=VoteSchema)
def vote_options(user_id, box_id, data):
    """
    Vote for ALL options in one box
    :param user_id: who is voting
    :param box_id: which box
    :param data:
        {
            "votes": {
                option_id: 0 - happy, 1 - neutral, 2 - sad
            }
        }
    """
    data = data['votes']

    # Validate the box_id
    if not validate_box_id(box_id):
        return jsonify({'message': 'Cannot find the wizbox'}), 404

    # Query all options of one box
    all_options = db.session.query(OptionModel).filter(OptionModel.box_id == box_id).all()

    # Validate the option in data
    option_id_list = [str(option.id) for option in all_options]
    if sorted(option_id_list) != sorted(list(data.keys())):
        return jsonify({"message": "Please vote all available options"}), 400

    # Get value of old vote
    vote = db.session.query(VoteModel).filter(VoteModel.box_id == box_id).filter(VoteModel.user_id == user_id).first()

    if request.method == "POST":
        if vote:
            return jsonify({"message": "Please choose the correct method"}), 400

        for option in all_options:
            option_id = str(option.id)
            # Update the vote value
            vote_value = data[option_id]
            option_vote_value = json.loads(option.vote)
            option_vote_value[vote_value] += 1
            option.vote = json.dumps(option_vote_value)
        db.session.commit()

        new_vote = VoteModel(user_id, box_id, json.dumps(data))
        db.session.add(new_vote)
        db.session.commit()
        return jsonify({"message": "Voted successfully"}), 201

    elif request.method == "PUT":
        if not vote:
            return jsonify({"message": "Please choose the correct method"}), 400
        
        vote_data = json.loads(vote.data)
        for option in all_options:
            option_id = str(option.id)

            # Update the vote value
            new_vote_value = data[option_id]
            old_vote_value = vote_data.get(option_id)
            option_vote_value = json.loads(option.vote)

            if old_vote_value is not None:
                option_vote_value[old_vote_value] -= 1

            option_vote_value[new_vote_value] += 1
            option.vote = json.dumps(option_vote_value)

        # Update vote data
        vote.data = json.dumps(data)
        db.session.commit()
        return jsonify({"message": "Update vote successfully"}), 200
