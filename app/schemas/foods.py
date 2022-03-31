import json

from marshmallow import fields, validate, post_load, pre_load

from .bases import Base


class FoodSchema(Base):
    name = fields.Str(required=True, validate=validate.Length(max=100, min=1))
    ingredients = fields.Str(required=True, validate=validate.Length(max=200, min=1))
    vegeterian = fields.Bool(required=True)
    origin = fields.Str(required=True, validate=validate.Length(max=200, min=1))
    preference = fields.Str(required=True, validate=validate.Length(max=200, min=1))
    cooking_method = fields.Str(required=True, validate=validate.Length(max=200, min=1))
    calories = fields.Int(required=True)

    @post_load
    def preprocess_ingredients(self, data, **kwargs):
        tmp = []
        ingredients_list = [i.strip() for i in list(data["ingredients"].split(","))]

        for ingredient in ingredients_list:
            ingredient_name = '_'.join(ingredient.split(" ")) if len(ingredient.split(" ")) > 0 else ingredient
            tmp.append(ingredient_name)

        data["ingredients"] = tmp
        data["name"] = data["name"].lower().strip().replace(" ", "_")
        return data
        

