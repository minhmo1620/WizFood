import random
import hashlib

from flask import Blueprint

auth = Blueprint('auth', __name__)


#create random salt
def create_salt():
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range (16):
        chars.append(random.choice(ALPHABET))
    return "".join(chars)


#hash password
def hash_password(users_password):
    # input: user password
    # then encode to convert into bytes
    return hashlib.sha256(users_password.encode('utf-8')).hexdigest()


@auth.route('/register')
def register():
    pass


@auth.route('/login')
def login():
    pass


@auth.route('/logout')
def logout():
    pass
