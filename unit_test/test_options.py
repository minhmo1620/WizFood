from flask import json

from unit_test.helpers import create_dummy_user, create_headers, create_dummy_box, create_dummy_option


def test_create_new_option(client):
    # create header
    token = create_dummy_user(username="mia", password="abc")
    headers = create_headers(token)
    box_id = create_dummy_box(1, "Minerva Feast", "06-02-2021")

    # invalid input
    data1 = {"name": 1, "description": "Vietnamese food"}
    response = client.post(f"/boxes/{box_id}/options", json=data1, headers=headers)
    assert response.status_code == 400
    assert {"name": ["Not a valid string."]} == json.loads(response.data)

    # invalid input
    data1 = {"name": "Ngon ngon", "description": 1}
    response = client.post(f"/boxes/{box_id}/options", json=data1, headers=headers)
    assert response.status_code == 400
    assert {"description": ["Not a valid string."]} == json.loads(response.data)

    # invalid box_id
    data1 = {"name": "Ngon ngon", "description": "Vietnamese food"}
    response = client.post("/boxes/10/options", json=data1, headers=headers)
    assert response.status_code == 404
    assert {'message': 'Cannot find the wizbox'} == json.loads(response.data)

    # valid input
    data1 = {"name": "Ngon ngon", "description": "Vietnamese food"}
    response = client.post(f"/boxes/{box_id}/options", json=data1, headers=headers)
    assert response.status_code == 201
    expected_response = {
        "name": "Ngon ngon",
        "description": "Vietnamese food",
        "id": 1
    }
    assert expected_response == json.loads(response.data)


def test_get_options(client):
    # create header
    token = create_dummy_user(username="mia", password="abc")
    headers = create_headers(token)
    box_id = create_dummy_box(1, "Minerva Feast", "06-02-2021")

    # create dummy options
    create_dummy_option(box_id, 1, "Option 1", "Description 1")
    create_dummy_option(box_id, 2, "Option 2", "Description 2")
    create_dummy_option(box_id, 3, "Option 3", "Description 3")
    create_dummy_option(box_id, 4, "Option 4", "Description 4")

    # invalid box_id
    response = client.get("/boxes/10/options", headers=headers)
    assert response.status_code == 404
    assert {'message': 'Cannot find the wizbox'} == json.loads(response.data)

    # valid box_id
    response = client.get(f'boxes/{box_id}/options', headers=headers)
    assert response.status_code == 200
    expected_response = [
        {
            'id': 1,
            'name': 'Option 1',
            'description': 'Description 1'
        },
        {
            'id': 2,
            'name': 'Option 2',
            'description': 'Description 2'
        },
        {
            'id': 3,
            'name': 'Option 3',
            'description': 'Description 3'
        },
        {
            'id': 4,
            'name': 'Option 4',
            'description': 'Description 4'
        }
    ]
    assert expected_response == json.loads(response.data)

