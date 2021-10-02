from flask import json

from unit_test.helpers import create_dummy_user


def test_create_user(client):
    """
    Test: Create a new user, "/users"
    """

    # invalid input
    data = {"username": 230, "password": "abc"}
    response = client.post("/users", json=data)
    assert response.status_code == 400
    expected_result = {"username": ["Not a valid string."]}
    assert expected_result == json.loads(response.data)

    # create a new user
    data = {"username": "mia", "password": "abc"}
    response = client.post("/users", json=data)
    assert response.status_code == 201
    assert "access_token" in json.loads(response.data)

    # existing user
    data = {"username": "mia", "password": "abcd"}
    response = client.post("/users", json=data)
    assert response.status_code == 400
    expected_result = {"message": "Existed username"}
    assert expected_result == json.loads(response.data)

    # empty input
    data = {"username": "mia", "password": ""}
    response = client.post("/users", json=data)
    assert response.status_code == 400
    expected_result = {"password": ["Length must be between 1 and 100."]}
    assert expected_result == json.loads(response.data)


def test_auth(client):
    """
    Test: Authorization, "/auth"
    """
    create_dummy_user(username="mia", password="abc")

    # valid user
    data = {"username": "mia", "password": "abc"}
    response = client.post("/auth", json=data)
    assert response.status_code == 200
    assert "access_token" in json.loads(response.data)

    # wrong password
    data = {"username": "mia", "password": "abcd"}
    response = client.post("/auth", json=data)
    assert response.status_code == 401
    expected_result = {"message": "Invalid username or password"}
    assert expected_result == json.loads(response.data)

    # user not found
    data = {"username": "abc", "password": "abc"}
    response = client.post("/auth", json=data)
    assert response.status_code == 401
    expected_result = {"message": "Invalid username or password"}
    assert expected_result == json.loads(response.data)
