import json
import subprocess

from flask import Blueprint, jsonify, current_app
from sqlalchemy import func
from multiprocessing import Lock

from app import db
from app.models.conversations import ConversationModel
from app.controllers.models import run_model
from app.schemas.conversations import ConversationSchema, UpdateConversationSchema
from app.helpers import validate_input

conversations_blueprint = Blueprint("conversations", __name__)

secret_key = current_app.config["SECRET_KEY"]

prologLock = Lock()


@conversations_blueprint.route("/conversations", methods=["POST"])
@validate_input(schema=ConversationSchema)
def create_new_conversation(data):
    new_conversation = ConversationModel(username=data['username'])
    db.session.add(new_conversation)
    db.session.commit()
    response = execute_models([])
    return jsonify({"message": response}), 201


@conversations_blueprint.route("/conversations", methods=["PUT"])
@validate_input(schema=UpdateConversationSchema)
def update_answer(data):
    username = data['username']
    answer = data['answer']

    conversation_id = db.session.query(func.max(ConversationModel.id)).filter(ConversationModel.username == username).first()
    conversation = db.session.query(ConversationModel).filter(ConversationModel.id == conversation_id[0]).first()

    answers = json.loads(conversation.answers)

    answers.append(answer)

    response = execute_models(answers)

    if response[:5] == 'Error':
        return jsonify({"message": response.split('\n')[0]}), 400

    conversation.answers = json.dumps(answers)
    db.session.commit()
    return jsonify({"message": response}), 200


def execute_models(user_answers):
    answers = ','.join(user_answers)
    create_command = "python app/controllers/models.py " + answers
    response = subprocess.run(create_command, shell=True, capture_output=True)
    return response.stdout.decode('UTF-8')
