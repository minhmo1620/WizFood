from flask import Blueprint, jsonify

from app import db
from app.models.foods import FoodModel
from app.models.knowledgebases import KnowledgeBaseModel
from app.helpers import validate_input, token_required

"""
In each box, user can add their food recommendation as an option for everyone to vote later
"""
foods_blueprint = Blueprint("foods", __name__)


@foods_blueprint.route("/foods", methods=["GET"])
@token_required
def get_foods(user_id):
    """
    Get all options of one box based on box_id
    """
    pass


@foods_blueprint.route("/foods", methods=["POST"])
@token_required
def create_new_option(user_id, data):
    """
    Create new option in one specific box
    """
    pass
