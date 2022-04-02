import json

import jwt
from flask import current_app
from app.models.foods import FoodModel

from app.models.users import UserModel
from app.models.boxes import BoxModel
from app.models.knowledgebases import KnowledgeBaseModel
from app.models.options import OptionModel
from app.helpers import hash_password, create_salt
from app.db import db


def create_dummy_user(username, password):
    user = db.session.query(UserModel).filter(UserModel.username == username).first()
    secret_key = current_app.config["SECRET_KEY"]
    if not user:
        salt = create_salt()
        hashed_password = hash_password(password + salt)

        new_user = UserModel(username, hashed_password, salt)

        token = jwt.encode({"user": username}, secret_key)

        db.session.add(new_user)
        db.session.commit()

        return token
    if user.password != hash_password(password + user.salt):
        return 401
    return jwt.encode({"user": username}, secret_key)

def create_dummy_user_with_knowledgeBase(username, password):
    token = create_dummy_user(username, password)

    user = db.session.query(UserModel).filter(UserModel.username == username).first()

    new_knowledge_base = KnowledgeBaseModel(user.id)
    db.session.add(new_knowledge_base)
    db.session.commit()

    return token, user.id

def create_headers(token):
    """
    This function will create headers for the request and will be called in other tests
    Normally, this function will be used to take the token from username and password to authenticate

    Input:
        - username
        - password
    Output: header
    """
    # data type in the body
    body_type = "application/json"

    # create header
    headers = {
        "Content-Type": body_type,
        "Authorization": "Bearer " + token
    }
    return headers


def create_dummy_box(user_id, name, description):
    """
    This function is to create a new wizbox in the database
    to test other functions for options/vote (get, put, post, delete)
    """
    new_box = BoxModel(user_id=user_id, name=name, description=description)

    db.session.add(new_box)
    db.session.commit()

    return new_box.id


def create_dummy_option(box_id, user_id, name, description):
    """
    This function is to create dummy option for specific wizbox
    """
    new_option = OptionModel(name, description, box_id, user_id)
    db.session.add(new_option)
    db.session.commit()


def get_current_votes(box_id):
    all_options = db.session.query(OptionModel).filter(OptionModel.box_id == box_id).all()
    votes = dict()

    for option in all_options:
        votes[option.id] = json.loads(option.vote)
    return votes

def get_all_foods(user_id):
    all_foods = db.session.query(FoodModel).filter(FoodModel.user_id == user_id).all()
    return all_foods