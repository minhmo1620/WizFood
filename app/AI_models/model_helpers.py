import json
from KB import *

def create_KB():
    foods = ""

    for food in food_data:
        foods += create_food_KB(food)
    
    calories_dict = create_categories_dict(food_data)

    askables = create_askables(askable_dict)

    KB = KB_headers + foods + calories_dict + calories_rules + askables + rules
    return KB

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

question = {
    'preference': 'What is your preference food?',
    'expected_calories': 'How many calories do you want to eat today?',
    'origin': 'Which country do you to have food today?',
    'spicy': 'Do you want spicy food',
    'noodle': 'Do you want some noodle?',
    'use_rice': 'Do you want rice?',
    'has_sambal': 'Do you want samble?',
    'contain_coconutmilk': 'Do you want food that contains coconutmilk?',
    'fry': 'Do you want fried food?',
    'soup': 'Do you want soup?',
    'contain_meat': 'Do you want meat in your meal?',
    'heavy_portion': 'Do you want heavy portion food?',
    'use_bread': 'Do you want to have bread?'
}