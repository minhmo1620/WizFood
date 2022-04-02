import json
from flask import Blueprint, jsonify

from app import db
from app.models.foods import FoodModel
from app.schemas.foods import FoodSchema
from app.helpers import validate_input, token_required

"""
This endpoint allows users to customize their own KB by adding new food
"""
foods_blueprint = Blueprint("foods", __name__)


@foods_blueprint.route("/foods", methods=["GET"])
# @token_required
def get_foods(user_id):
    """
    Get all foods created by this user
    """
    #TODO: Implement this if necessary
    pass


@foods_blueprint.route("/foods", methods=["POST"])
@token_required
@validate_input(schema=FoodSchema)
def create_new_food(user_id, data):
    """
    Create new food
    Inputs:
        - name (str, required): The name of the food
        - ingredients (str, required): List of ingredients, separated by comma
        - calories (int): The calories of food. Default calories = 0.
        - preference (str): The type of food cuisine
        - origin (str): The country origin of the food
        - cooking_method (str): Cooking method of the food
    """
    # Create food_data based on the inputs (only add fields that are not empty string)
    food_data = {
        "name": data["name"],
        "ingredients": data["ingredients"],
        "calories": int(data["calories"]) if "calories" in data else 0
    }

    for k in ["preference", "origin", "cooking_method"]:
        if k in data and len(data[k]) > 0:
            food_data[k] = data[k]

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
