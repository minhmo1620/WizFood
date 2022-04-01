import json
from flask import Blueprint, jsonify

from app import db
from app.models.foods import FoodModel
from app.schemas.foods import FoodSchema
from app.helpers import validate_input, token_required

"""

"""
foods_blueprint = Blueprint("foods", __name__)


@foods_blueprint.route("/foods", methods=["GET"])
# @token_required
def get_foods(user_id):
    """

    """
    pass


@foods_blueprint.route("/foods", methods=["POST"])
@token_required
@validate_input(schema=FoodSchema)
def create_new_food(user_id, data):
    """

    """
    food_data = {
        "name": data["name"],
        "preference": data["preference"],
        "origin": data["origin"],
        "ingredients": data["ingredients"],
        "vegeterian": "yes" if data["vegeterian"] else "no",
        "cooking_method": data["cooking_method"],
        "calories": data["calories"]
    }

    # Check existing food
    food = db.session.query(FoodModel).\
        filter(FoodModel.user_id == user_id, FoodModel.name == data["name"]).first()
    if food:
        return jsonify({"message": "Existed food"}), 400

    # Create new food
    new_food = FoodModel(user_id, data["name"], json.dumps(food_data))
    db.session.add(new_food)
    db.session.commit()

    return jsonify({"message": "Added the food to the knowledge base successfully"}), 201
