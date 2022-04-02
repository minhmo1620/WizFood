import json

from unit_test.helpers import create_headers, create_dummy_user_with_knowledgeBase, get_all_foods

def test_create_new_food(client):
    token, user_id = create_dummy_user_with_knowledgeBase(username="mia", password="abc")
    headers = create_headers(token)

    # No food in the data yet
    all_foods = get_all_foods(user_id)

    assert len(all_foods) == 0

    # invalid data - Missing required field
    data = {
        "name": "fried chicken"
    }
    response = client.post("/foods", json=data, headers=headers)
    assert response.status_code == 400
    expected_response = {
        'ingredients': ['Missing data for required field.']
    }
    assert expected_response == json.loads(response.data)

    data = {
        "ingredients": "chicken, flour"
    }
    response = client.post("/foods", json=data, headers=headers)
    assert response.status_code == 400
    expected_response = {
        'name': ['Missing data for required field.']
    }
    assert expected_response == json.loads(response.data)

    # valid input
    data = {
        "name": "fried chicken",
        "ingredients": "chicken, flour"
    }
    response = client.post("/foods", json=data, headers=headers)
    assert response.status_code == 201
    expected_response = {
        "message": "Added the food to the knowledge base successfully"
    }
    assert expected_response == json.loads(response.data)

    all_foods = get_all_foods(user_id)
    assert len(all_foods) == 1
    food = all_foods[0]
    assert food.name == "fried_chicken"
    expected_data_store = {
        "name": "fried_chicken",
        "ingredients": ["chicken", "flour"],
        "calories": 0
    }
    assert expected_data_store == json.loads(food.data)

    # repeat the request - should not have the same food name
    data = {
        "name": "fried chicken",
        "ingredients": "chicken, flour, egg"
    }
    response = client.post("/foods", json=data, headers=headers)
    assert response.status_code == 400
    expected_response = {
        "message": "Existed food"
    }
    assert expected_response == json.loads(response.data)

    # One more food with full data
    data = {
        "name": "avocado toast",
        "ingredients": "avocado, bread",
        "calories": 600,
        "cooking_method": "toast",
        "preference": "",
        "origin": ""
    }
    response = client.post("/foods", json=data, headers=headers)
    assert response.status_code == 201
    expected_response = {
        "message": "Added the food to the knowledge base successfully"
    }
    assert expected_response == json.loads(response.data)

    all_foods = get_all_foods(user_id)
    assert len(all_foods) == 2

    food0 = all_foods[0]
    assert food0.name == "fried_chicken"
    expected_data_store = {
        "name": "fried_chicken",
        "ingredients": ["chicken", "flour"],
        "calories": 0
    }
    assert expected_data_store == json.loads(food0.data)

    food1 = all_foods[1]
    assert food1.name == "avocado_toast"
    expected_data_store = {
        "name": "avocado_toast",
        "ingredients": ["avocado", "bread"],
        "calories": 600,
        "cooking_method": "toast"
    }
    assert expected_data_store == json.loads(food1.data)
