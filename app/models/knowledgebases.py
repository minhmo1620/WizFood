import json

from app import db
from app.models.foods import FoodModel
from KB import KB_headers, calories_rules, rules, food_data


class KnowledgeBaseModel(db.Model):
    __tablename__ = "knowledgebases"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    kb = db.Column(db.Text, nullable=False)
    foods = db.Column(db.Text, nullable=False)
    askable_dict = db.Column(db.Text, nullable=False)
    
    kb_header = db.Column(db.Text, nullable=False)
    calories_rules = db.Column(db.Text, nullable=False)
    rules = db.Column(db.Text, nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id
        self.foods = json.dumps(food_data)
        self.askable_dict = json.dumps(create_askable_dict(food_data))
        self.kb_header = KB_headers
        self.calories_rules = calories_rules
        self.rules = rules
        self.kb = self.update_kb()
    
    def update_kb(self):
        # Get up-to-date food data of that user
        user_food = get_food_data(self.user_id)
        self.foods = json.dumps(food_data + user_food)

        # Create foods_data (str)
        foods_data = ""
        for food in json.loads(self.foods):
            foods_data += create_food_KB(food)
        
        # Create calories_dict
        calories_dict = create_categories_dict(json.loads(self.foods))

        # Update the askable_dict
        self.update_askable_dict()

        # Create askables (str)
        askables = create_askables(json.loads(self.askable_dict))

        # Update the KB
        self.kb = json.dumps(self.kb_header + foods_data + calories_dict + self.calories_rules + askables + self.rules)
        
        return self.kb
    
    def update_askable_dict(self):
        self.askable_dict = json.dumps(create_askable_dict(json.loads(self.foods)))
    
    def get_questions_dict(self):
        questions_dict = {}
        askable_dict = json.loads(self.askable_dict)
        for k, v in askable_dict.items():
            questions_dict[k] = v["question"]
        
        return questions_dict

def get_food_data(user_id):
    list_foods = db.session.query(FoodModel).filter(FoodModel.user_id == user_id).all()

    return [json.loads(food.data) for food in list_foods]

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


def create_askable_dict(food_data):
    askable_dict = {
        "preference": {
            "type":"menuask",
            "question": "What is your preference food cuisine today?",
            "choices": []
        },
        "expected_calories": {
            "type": "numberask",
            "question" : "How many calories do you want today?"
        },
        "origin": {
            "type": "menuask",
            "question": "Which country do you want to have food today?",
            "choices": []
        },
        "cooking_method": {
            "type": "menuask",
            "question": "Please choose your prefered cooking method",
            "choices": []
        }
    }

    for food in food_data:
        for k, v in food.items():
            if k == "name" or k == "calories":
                continue
            elif k == "ingredients":
                for ingredient in v:
                    if ingredient not in askable_dict:
                        ingredient_name = format_food_name(ingredient)
                        askable_dict[ingredient] = {
                            "type": "ask",
                            "question": f"Do you want to have food with {ingredient_name} today?"
                        }
            elif k in ["preference", "origin", "cooking_method"]:
                if v not in askable_dict[k]["choices"]:
                    askable_dict[k]["choices"].append(v)
            
            else:
                if k not in askable_dict:
                    display_name = format_food_name(k)
                    askable_dict[k] = {
                        "type": "ask",
                        "question": f"Do you want {display_name} today?"
                    }
    return askable_dict

def format_food_name(food_name):
    return ' '.join(food_name.split('_'))