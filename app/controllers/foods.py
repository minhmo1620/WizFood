from flask import Blueprint, jsonify

from app import db
from app.models.foods import FoodModel
from app.models.knowledgebases import KnowledgeBaseModel
from app.helpers import validate_input, token_required

"""

"""
foods_blueprint = Blueprint("foods", __name__)


@foods_blueprint.route("/foods", methods=["GET"])
@token_required
def get_foods(user_id):
    """

    """
    pass


@foods_blueprint.route("/foods", methods=["POST"])
@token_required
def create_new_option(user_id, data):
    """

    """
    pass
