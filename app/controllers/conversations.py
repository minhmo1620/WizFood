import json
import subprocess

from flask import Blueprint, jsonify, current_app
from sqlalchemy import func

from app import db
from app.models.conversations import ConversationModel
from app.schemas.conversations import UpdateConversationSchema
from app.helpers import token_required, validate_input

conversations_blueprint = Blueprint("conversations", __name__)

secret_key = current_app.config["SECRET_KEY"]


@conversations_blueprint.route("/conversations", methods=["POST"])
@token_required
def create_new_conversation(user_id):
    """
    Create a new conversation between user and WizAid
    :param data: {}
    :return: {
        "message": <the first question sending to user>
    }
    """
    # Create new conversation based on username
    new_conversation = ConversationModel(user_id = user_id)
    db.session.add(new_conversation)
    db.session.commit()

    # Run model to have the first question
    response = execute_models([])
    return jsonify(json.loads(response)), 201


@conversations_blueprint.route("/conversations", methods=["PUT"])
@token_required
@validate_input(schema=UpdateConversationSchema)
def update_answer(user_id, data):
    """
    Update the conversation in WizAId
    :param data: a dictionary with
        - 'answer': the answer of user for current question
    :return:
        - (str) the response of the chatbot regarding to user's answer provided
    """
    answer = data['answer']
    print('answer', answer)

    # Query the latest conversation of current username
    conversation_id = db.session.query(func.max(ConversationModel.id)).filter(
        ConversationModel.user_id == user_id).first()
    conversation = db.session.query(ConversationModel).filter(ConversationModel.id == conversation_id[0]).first()

    # Loads the existed answers list
    answers = json.loads(conversation.answers)

    # Append new answer to answers list
    answers.append(answer)
    print("answers", answers)
    print("answers_type", type(answers))

    # Run model to get the next question
    response = execute_models(answers)
    print('response', response)

    # If user's answer is not validated
    if response[:5] == 'Error':
        return jsonify({"message": response.split('\n')[0]}), 400

    # If the user's answer is accepted, return the question
    conversation.answers = json.dumps(answers)
    db.session.commit()
    return jsonify(json.loads(response)), 200


def execute_models(user_answers):
    # Join the list of answers to a string format a,b,c
    answers = ','.join(user_answers)
    # Create shell command
    create_command = "python app/AI_models/models.py " + answers
    # Run model with answers as argument
    response = subprocess.run(create_command, shell=True, capture_output=True)
    return response.stdout.decode('UTF-8')
