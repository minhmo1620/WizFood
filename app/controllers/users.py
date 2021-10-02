from flask import Blueprint, jsonify, current_app

from app import db
from app.models.users import UserModel
from app.schemas.users import UserSchema
from app.helpers import hash_password, validate_input, create_salt, encode

users_blueprint = Blueprint("users", __name__)

secret_key = current_app.config["SECRET_KEY"]


@users_blueprint.route("/users", methods=["POST"])
@validate_input(schema=UserSchema)
def create_user(data):
    """
    input:
        - username: string
        - password: string
    output:
        - return error if username is existed
        - if username is not existed
            - create new salt
            - hash password
            --> create new user (username, hashed password, salt)
    """
    username = data["username"]
    password = data["password"]

    user = db.session.query(UserModel).filter(UserModel.username == username).first()
    if user:
        return jsonify({"message": "Existed username"}), 400

    salt = create_salt()
    hashed_password = hash_password(password + salt)

    new_user = UserModel(username, hashed_password, salt)
    db.session.add(new_user)
    db.session.commit()

    token = encode(new_user).decode("UTF-8")
    return jsonify({"access_token": token}), 201


@users_blueprint.route("/auth", methods=["POST"])
@validate_input(schema=UserSchema)
def auth(data):
    """
    input:
        - username
        - password
    output:
        - token
    """
    username = data["username"]
    password = data["password"]

    user = db.session.query(UserModel).filter(UserModel.username == username).first()

    if not user or hash_password(password + user.salt) != user.password:
        return jsonify({"message": "Invalid username or password"}), 401

    token = encode(user).decode("UTF-8")
    return jsonify({"access_token": token}), 200
