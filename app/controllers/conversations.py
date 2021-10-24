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
    # new_conversation = ConversationModel(username=data['username'])
    # db.session.add(new_conversation)
    # db.session.commit()
    # print("Hi")
    response = execute_models([])
    return jsonify({"message": response}), 201


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


def execute_models(user_answers):
    answers = ','.join(user_answers)
    create_command = "python app/controllers/models.py " + answers + " 2>'./output.txt'"
    subprocess.call(create_command, shell=True)
    filename = './output.txt'

    response = ""
    with open(filename) as file:
        while line := file.readline().rstrip():
            if line[:7] == "Warning":
                continue
            response += line
            response += '\n'
    return response
