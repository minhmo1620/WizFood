import json

from marshmallow import fields, validate, post_load, pre_load

from .bases import Base


class FoodSchema(Base):
    name = fields.Str(required=True, validate=validate.Length(max=100, min=1))
    ingredients = fields.Str(required=True, validate=validate.Length(max=200, min=1))
    origin = fields.Str(required=False, validate=validate.Length(max=200, min=1))
    preference = fields.Str(required=False, validate=validate.Length(max=200, min=1))
    cooking_method = fields.Str(required=False, validate=validate.Length(max=200, min=1))
    calories = fields.Int(required=False)

    @post_load
    def preprocess_ingredients(self, data, **kwargs):
        tmp = []
        ingredients_list = [i.strip() for i in list(data["ingredients"].split(","))]

        for ingredient in ingredients_list:
            ingredient_name = format_data(ingredient)
            tmp.append(ingredient_name)

        data["ingredients"] = tmp
        data["name"] = format_data(data["name"])

        for k in ["origin", "preference", "cooking_method"]:
            if k in data:
                data[k] = format_data(data[k])
        return data
        
def format_data(data):
    return data.lower().strip().replace(" ", "_")