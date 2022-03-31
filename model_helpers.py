import json

from KB import *
from app.models.knowledgebases import KnowledgeBaseModel
from app.db import db

def create_KB(user_id):
    knowledgebase = db.session.query(KnowledgeBaseModel).filter_by(user_id=user_id).first()
    knowledgebase.update_kb()
    db.session.commit()
    return json.loads(knowledgebase.kb)

def get_questions_dict(user_id):
    knowledgebase = db.session.query(KnowledgeBaseModel).filter_by(user_id=user_id).first()
    return knowledgebase.get_questions_dict()

def create_ask_question(A, V, question):
    """
    Create question to ask users includes 
    - questions for askables
    - options with numbered list
    - error for previous input
    """
    if str(A) == 'ingredient':
        askable_question = 'Do you want ' + str(V) +' ?'
    else:
        askable_question = str(question[str(A)])
    return json.dumps({
        "message": askable_question,
        "options": ["yes", "no"]
    })
    
def create_numberask_question(A, question):
    """
    Create questions to ask for number
    """
    askable_question = question[str(A)]+'\n'+'Your answer is: ' if str(A) in question else str(A)
    return json.dumps({
        "message": askable_question,
        "options": []
    })

def create_menuask_question(A, menu, question):
    """
    Create questions to have menuasks
    """
    menuask_question = question[str(A)]
    menu_list = [str(i) for i in menu]
    
    return json.dumps({
        "message": menuask_question,
        "options": menu_list
    })
