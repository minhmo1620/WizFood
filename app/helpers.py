import hashlib
import random
from functools import wraps
from string import digits, ascii_letters

import jwt
from flask import jsonify, request, current_app
from marshmallow import ValidationError

from app.models.users import UserModel
from .db import db


def encode(user):
    return jwt.encode({"user": user.username}, current_app.config["SECRET_KEY"], algorithm="HS256")


def hash_password(user_password):
    return hashlib.sha256(user_password.encode("utf-8")).hexdigest()


def token_required(f):
    """
    Decorator to validate the token and return user_id
    """

    @wraps(f)
    def wrapper(*arg, **kwargs):
        if not request.headers.get("Authorization"):
            return jsonify({"message": "Authorization required"}), 400

        token = request.headers["Authorization"].split()
        if token[0] != "Bearer":
            return jsonify({"message": "Invalid token"}), 400
        try:
            data = jwt.decode(token[1], current_app.config["SECRET_KEY"], algorithms=["HS256"])
            username = data["user"]
            user = db.session.query(UserModel).filter_by(username=username).first()
            if user is None:
                return jsonify({"message": "Unauthenticated"}), 401
        except:
            return jsonify({"message": "Invalid token"}), 400
        return f(*arg, **kwargs, user_id=user.id)

    return wrapper


def validate_input(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # take the input
            data = request.get_json()
            if (data is None) or (data == {}):
                return jsonify({"message": "Data is required."}), 400

            # check the validity of the input
            try:
                data = schema().load(data)
            except ValidationError as err:
                return jsonify(err.messages), 400
            return f(*args, **kwargs, data=data)
        return wrapper
    return decorator


def create_salt():
    """
    Create a random salt with 16 characters long
    """
    characters = digits + ascii_letters
    chars = random.choices(characters, k=16)
    return "".join(chars)
