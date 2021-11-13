import json
import subprocess

from flask import Blueprint, jsonify, current_app
from sqlalchemy import func

from app import db
from app.models.conversations import ConversationModel
from app.schemas.conversations import ConversationSchema, UpdateConversationSchema
from app.helpers import validate_input

conversations_blueprint = Blueprint("conversations", __name__)

secret_key = current_app.config["SECRET_KEY"]


@conversations_blueprint.route("/conversations", methods=["POST"])
@validate_input(schema=ConversationSchema)
def create_new_conversation(data):
    # Create new conversation based on username
    new_conversation = ConversationModel(username=data['username'])
    db.session.add(new_conversation)
    db.session.commit()

    # Run model to have the first question
    response = execute_models([])
    return jsonify({"message": response}), 201


@conversations_blueprint.route("/conversations", methods=["PUT"])
@validate_input(schema=UpdateConversationSchema)
def update_answer(data):
    username = data['username']
    answer = data['answer']

    # Query the latest conversation of current username
    conversation_id = db.session.query(func.max(ConversationModel.id)).filter(
        ConversationModel.username == username).first()
    conversation = db.session.query(ConversationModel).filter(ConversationModel.id == conversation_id[0]).first()

    # Loads the existed answers list
    answers = json.loads(conversation.answers)

    # Append new answer to answers list
    answers.append(answer)

    # Run model to get the next question
    response = execute_models(answers)

    # If user's answer is not validated
    if response[:5] == 'Error':
        return jsonify({"message": response.split('\n')[0]}), 400

    # If the user's answer is accepted, return the question
    conversation.answers = json.dumps(answers)
    db.session.commit()
    return jsonify({"message": response}), 200


def execute_models(user_answers):
    # Join the list of answers to a string format a,b,c
    answers = ','.join(user_answers)
    # Create shell command
    create_command = "python app/controllers/models.py " + answers
    # Run model with answers as argument
    response = subprocess.run(create_command, shell=True, capture_output=True)
    return response.stdout.decode('UTF-8')
