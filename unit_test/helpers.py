import jwt
from flask import current_app

from app.models.users import UserModel
from app.helpers import hash_password, create_salt
from app.db import db

secret_key = current_app.config["SECRET_KEY"]


def create_dummy_user(username, password):
    user = db.session.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        salt = create_salt()
        hashed_password = hash_password(password + salt)

        new_user = UserModel(username, hashed_password, salt)

        token = jwt.encode({"user": username}, secret_key).decode("UTF-8")

        db.session.add(new_user)
        db.session.commit()

        return token
    if user.password != hash_password(password + user.salt):
        return 401
    return jwt.encode({"user": username}, secret_key).decode("UTF-8")


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

