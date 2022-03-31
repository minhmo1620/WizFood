import json

from KB import *
from app.models.knowledgebases import KnowledgeBaseModel
from app.db import db

def create_KB(user_id):
    knowledgebase = db.session.query(KnowledgeBaseModel).filter_by(user_id=user_id).first()
    return knowledgebase.update_kb()

def create_food_KB(food):
    name = food["name"]
    food_str = f"\nfood({name}) :- "
    for k, v in food.items():
        if k == "name" or k == "calories":
            continue
        elif k == "ingredients":
            for ingredient in v:
                food_str += f"\n    {ingredient}(yes),"
        else:
            food_str += f"\n    {k}({v}),"
    
    food_str = food_str[:-1] + ".\n"
    return food_str

def create_categories_dict(food_data):
    str_dict = "{"
    for food in food_data:
        name = food["name"]
        calories = food["calories"]
        str_dict += f"\n    {name}: {calories},"
    str_dict = str_dict[:-1] + " \n}"
    return f"\nmy_dict(_{str_dict}).\n"

def create_askables(askable_dict):
    askables = "\n% Askables\n"
    for k, v in askable_dict.items():
        if v["type"] == "numberask":
            askables += f"{k}(X) :- numberask({k}, X).\n"
        elif v["type"] == "menuask":
            choices = convert_list_to_str(v["choices"])
            askables += f"{k}(P):- menuask({k}, P, {choices}).\n"
        elif v["type"] == "ask":
            askables += f"{k}(X) :- ask({k}, X).\n"
    return askables

def convert_list_to_str(a):
    res = "["
    for i in a:
        res += i
        res += ', '
    res = res[:-2] + ']'
    return res


def create_ask_question(A, V):
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
    
def create_numberask_question(A):
    """
    Create questions to ask for number
    """
    askable_question = question[str(A)]+'\n'+'Your answer is: ' if str(A) in question else str(A)
    return json.dumps({
        "message": askable_question,
        "options": []
    })

def create_menuask_question(A, menu):
    """
    Create questions to have menuasks
    """
    menuask_question = question[str(A)]
    menu_list = [str(i) for i in menu]
    
    return json.dumps({
        "message": menuask_question,
        "options": menu_list
    })
