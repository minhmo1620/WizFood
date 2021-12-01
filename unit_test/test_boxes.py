from flask import json

from unit_test.helpers import create_dummy_user, create_headers, create_dummy_box


def test_create_new_box(client):
    """
    Test: Create a new wizbox POST "boxes"
    """
    # create header
    token = create_dummy_user(username="mia", password="abc")
    headers = create_headers(token)

    # no data
    response = client.post("/boxes", headers=headers)
    assert response.status_code == 400
    assert {'message': '400 Bad Request: Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)'} \
           == json.loads(response.data)

    # empty data
    response = client.post("/boxes", json={}, headers=headers)
    assert response.status_code == 400
    assert {"message": "Data is required."} == json.loads(response.data)

    # invalid input
    data = {"name": 1, "description": "Vietnamese food"}
    response = client.post("/boxes", json=data, headers=headers)
    assert response.status_code == 400
    assert {"name": ["Not a valid string."]} == json.loads(response.data)

    # invalid input
    data = {"name": "Minerva Feast", "description": 1.2}
    response = client.post("/boxes", json=data, headers=headers)
    assert response.status_code == 400
    assert {"description": ["Not a valid string."]} == json.loads(response.data)

    # valid input
    data = {"name": "Minerva Feast", "description": "06-02-2020"}
    response = client.post("/boxes", json=data, headers=headers)
    assert response.status_code == 201
    expected_response = {
        "name": "Minerva Feast",
        "description": "06-02-2020",
        "id": 1,
    }
    assert expected_response == json.loads(response.data)


def test_get_all_boxes(client):
    token = create_dummy_user(username="mia", password="abc")
    headers = create_headers(token)

    create_dummy_box(1, "Box 1", "Description 1")
    create_dummy_box(1, "Box 2", "Description 2")
    create_dummy_box(1, "Box 3", "Description 3")
    create_dummy_box(2, "Box 4", "Description 4")

    response = client.get('/boxes', headers=headers)
    assert response.status_code == 200
    expected_response = [
        {
            "id": 1,
            "name": "Box 1",
            "description": "Description 1"
        },
        {
            "id": 2,
            "name": "Box 2",
            "description": "Description 2"
        },
        {
            "id": 3,
            "name": "Box 3",
            "description": "Description 3"
        }
    ]
    assert expected_response == json.loads(response.data)
