import threading
from multiprocessing import Pool

from flask import Blueprint, jsonify, current_app, render_template, request
from sqlalchemy import func
from multiprocessing import Lock

from app import db
from app.models.conversations import ConversationModel
from app.controllers.models import run_model
from app.schemas.conversations import ConversationSchema, UpdateConversationSchema
from app.helpers import validate_input

import tempfile
from pyswip.prolog import Prolog
from pyswip.easy import *

from app.controllers.model_helpers import create_ask_question, create_menuask_question, create_numberask_question
from app.controllers.KB import ModelConfig
# from app.controllers.test import model_pool

conversations_blueprint = Blueprint("conversations", __name__)

secret_key = current_app.config["SECRET_KEY"]


@conversations_blueprint.route("/conversations", methods=["POST"])
@validate_input(schema=ConversationSchema)
def create_new_conversation(data):
    # new_conversation = ConversationModel(username=data['username'])
    # db.session.add(new_conversation)
    # db.session.commit()
    run_model(["asian", "yes", "no", "yes", "yes", "vietnam", 600])

    return jsonify({"message": "1"}), 201


@conversations_blueprint.route("/conversations", methods=["PUT"])
@validate_input(schema=UpdateConversationSchema)
def update_answer(data):
    username = data['username']
    answer = data['answer']

    conversation_id = db.session.query(func.max(ConversationModel.id)).filter(ConversationModel.username == username).all()
    conversation = db.session.query(ConversationModel).filter(ConversationModel.id == conversation_id).all()

    answers = conversation.answers

    answers.append(answer)

    response = run_model(answers)

    return jsonify({"message": response})



# run_model(["asian", "yes", "no", "yes", "yes", "vietnam", 600])

