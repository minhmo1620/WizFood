from flask import json

from unit_test.helpers import create_dummy_user, create_headers, create_dummy_box, create_dummy_option, \
    get_current_votes, create_vote

def test_get_vote_data(client):
    # Set up the box
    token = create_dummy_user(username="mia", password="abc")
    headers = create_headers(token)
    box_id = create_dummy_box(1, "Minerva Feast", "06-02-2021")

    # Add options into the box
    create_dummy_option(box_id, 1, "Option 1", "Description 1")
    create_dummy_option(box_id, 2, "Option 2", "Description 2")
    create_dummy_option(box_id, 3, "Option 3", "Description 3")
    create_dummy_option(box_id, 4, "Option 4", "Description 4")

    # Invalid box id
    response = client.get('/boxes/10/vote', headers=headers)
    assert response.status_code == 404
    assert {'message': 'Cannot find the wizbox'} == json.loads(response.data)

    # No vote
    response = client.get(f'/boxes/{box_id}/vote', headers=headers)
    assert response.status_code == 200
    assert {} == json.loads(response.data)

    # Vote
    data = {
        1: 0,
        2: 1,
        3: 1,
        4: 1
    }
    create_vote(1, box_id, data)
    create_vote(2, box_id, data)

    # Get vote data
    response = client.get(f'/boxes/{box_id}/vote', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data) == {
        "id": 1,
        "data": {
            "1": 0,
            "2": 1,
            "3": 1,
            "4": 1
        }
    }

def test_vote_options_fail(client):
    # create header
    token = create_dummy_user(username="mia", password="abc")
    headers = create_headers(token)
    box_id = create_dummy_box(1, "Minerva Feast", "06-02-2021")

    # invalid data
    data = {
        "votes": {
            1: 0,
            2: 1
        }
    }

    response = client.post(f'/boxes/{box_id}/vote', json=data, headers=headers)
    assert response.status_code == 400
    assert {"message": "Please vote all available options"} == json.loads(response.data)

    create_dummy_option(box_id, 1, "Option 1", "Description 1")
    create_dummy_option(box_id, 2, "Option 2", "Description 2")
    create_dummy_option(box_id, 3, "Option 3", "Description 3")
    create_dummy_option(box_id, 4, "Option 4", "Description 4")

    # invalid data
    data = {
        "votes": {
            1: 0,
            2: 1
        }
    }

    response = client.post(f'/boxes/{box_id}/vote', json=data, headers=headers)
    assert response.status_code == 400
    assert {"message": "Please vote all available options"} == json.loads(response.data)

    # invalid data
    data = {
        "votes": {
            1: 0,
            5: 1
        }
    }

    response = client.post(f'/boxes/{box_id}/vote', json=data, headers=headers)
    assert response.status_code == 400
    assert {"message": "Please vote all available options"} == json.loads(response.data)

    # invalid data
    data = {
        "votes": {
            1: 0,
            2: 3
        }
    }

    response = client.post(f'/boxes/{box_id}/vote', json=data, headers=headers)
    assert response.status_code == 400
    expected_response = {
        'votes': {
            '2': {
                'value':
                    ['Must be greater than or equal to 0 and less than or equal to 2.']
            }
        }
    }
    assert expected_response == json.loads(response.data)

    # invalid data
    data = {
        "votes": {
            1: -1,
            2: 3
        }
    }

    response = client.post(f'/boxes/{box_id}/vote', json=data, headers=headers)
    assert response.status_code == 400
    expected_response = {
        'votes': {
            '1': {
                'value':
                    ['Must be greater than or equal to 0 and less than or equal to 2.']
            },
            '2': {
                'value':
                    ['Must be greater than or equal to 0 and less than or equal to 2.']
            }
        }
    }
    assert expected_response == json.loads(response.data)

    # invalid box_id
    data = {
        "votes": {
            1: 0,
            2: 1,
            3: 1,
            4: 1
        }
    }

    response = client.post(f'/boxes/10/vote', json=data, headers=headers)
    assert response.status_code == 404
    assert {'message': 'Cannot find the wizbox'} == json.loads(response.data)

    # no data
    response = client.post(f'/boxes/{box_id}/vote', headers=headers)
    assert response.status_code == 400
    assert {'message': '400 Bad Request: Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)'} \
           == json.loads(response.data)

    # empty data
    response = client.post(f'/boxes/{box_id}/vote', json={}, headers=headers)
    assert response.status_code == 400
    assert {"message": "Data is required."} == json.loads(response.data)


def test_vote_option_success(client):
    # create header
    # user 1
    token1 = create_dummy_user(username="mia", password="abc")
    headers1 = create_headers(token1)
    # user 2
    token2 = create_dummy_user(username="minh", password="abc")
    headers2 = create_headers(token2)

    # Create a new box
    box_id = create_dummy_box(1, "Minerva Feast", "06-02-2021")

    create_dummy_option(box_id, 1, "Option 1", "Description 1")
    create_dummy_option(box_id, 2, "Option 2", "Description 2")
    create_dummy_option(box_id, 3, "Option 3", "Description 3")
    create_dummy_option(box_id, 4, "Option 4", "Description 4")

    # valid data
    all_votes_before = get_current_votes(box_id)
    expected_all_votes_before = {
        1: [0, 0, 0],
        2: [0, 0, 0],
        3: [0, 0, 0],
        4: [0, 0, 0]
    }
    assert expected_all_votes_before == all_votes_before

    data = {
        "votes": {
            1: 0,
            2: 1,
            3: 1,
            4: 1
        }
    }

    response = client.post(f'/boxes/{box_id}/vote', json=data, headers=headers1)
    assert response.status_code == 201
    assert {"message": "Voted successfully"} == json.loads(response.data)

    all_votes_after = get_current_votes(box_id)
    expected_all_votes_after = {
        1: [1, 0, 0],
        2: [0, 1, 0],
        3: [0, 1, 0],
        4: [0, 1, 0]
    }
    assert expected_all_votes_after == all_votes_after

    # one more vote
    all_votes_before = get_current_votes(box_id)
    expected_all_votes_before = {
        1: [1, 0, 0],
        2: [0, 1, 0],
        3: [0, 1, 0],
        4: [0, 1, 0]
    }
    assert expected_all_votes_before == all_votes_before

    data = {
        "votes": {
            1: 1,
            2: 2,
            3: 0,
            4: 1
        }
    }

    response = client.post(f'/boxes/{box_id}/vote', json=data, headers=headers1)
    assert response.status_code == 400
    assert {"message": "Please choose the correct method"} == json.loads(response.data)

    response = client.put(f'/boxes/{box_id}/vote', json=data, headers=headers1)
    assert response.status_code == 200
    assert {"message": "Update vote successfully"} == json.loads(response.data)

    all_votes_after = get_current_votes(box_id)
    expected_all_votes_after = {
        1: [0, 1, 0],
        2: [0, 0, 1],
        3: [1, 0, 0],
        4: [0, 1, 0]
    }
    assert expected_all_votes_after == all_votes_after

    # Add new options
    create_dummy_option(box_id, 1, "Option 5", "Description 5")
    create_dummy_option(box_id, 2, "Option 6", "Description 6")

    # one vote from user 1 after adding new options
    all_votes_before = get_current_votes(box_id)
    expected_all_votes_before = {
        1: [0, 1, 0],
        2: [0, 0, 1],
        3: [1, 0, 0],
        4: [0, 1, 0],
        5: [0, 0, 0],
        6: [0, 0, 0]
    }
    assert expected_all_votes_before == all_votes_before

    data = {
        "votes": {
            1: 1,
            2: 2,
            3: 0,
            4: 1,
            # Add vote for new options
            5: 1,
            6: 0
        }
    }

    response = client.put(f'/boxes/{box_id}/vote', json=data, headers=headers1)
    assert response.status_code == 200
    assert {"message": "Update vote successfully"} == json.loads(response.data)

    all_votes_after = get_current_votes(box_id)
    expected_all_votes_after = {
        1: [0, 1, 0],
        2: [0, 0, 1],
        3: [1, 0, 0],
        4: [0, 1, 0],
        5: [0, 1, 0],
        6: [1, 0, 0]
    }
    assert expected_all_votes_after == all_votes_after

    # Vote from user 2 after adding new options
    all_votes_before = get_current_votes(box_id)
    expected_all_votes_before = {
        1: [0, 1, 0],
        2: [0, 0, 1],
        3: [1, 0, 0],
        4: [0, 1, 0],
        5: [0, 1, 0],
        6: [1, 0, 0]
    }
    assert expected_all_votes_before == all_votes_before

    data = {
        "votes": {
            1: 1,
            2: 2,
            3: 0,
            4: 1,
            5: 1,
            6: 0
        }
    }

    response = client.post(f'/boxes/{box_id}/vote', json=data, headers=headers2)
    assert response.status_code == 201
    assert {"message": "Voted successfully"} == json.loads(response.data)

    all_votes_after = get_current_votes(box_id)
    expected_all_votes_after = {
        1: [0, 2, 0],
        2: [0, 0, 2],
        3: [2, 0, 0],
        4: [0, 2, 0],
        5: [0, 2, 0],
        6: [2, 0, 0]
    }
    assert expected_all_votes_after == all_votes_after
