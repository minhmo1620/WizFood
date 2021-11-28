from flask import json

from unit_test.helpers import create_dummy_user, create_headers, create_dummy_box, create_dummy_option, \
    get_current_votes


def test_vote_options_fail(client):
    # create header
    token = create_dummy_user(username="mia", password="abc")
    headers = create_headers(token)
    box_id = create_dummy_box(1, "Minerva Feast", "06-02-2021")

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
    assert {"message": "Please vote for all options"} == json.loads(response.data)

    # invalid data
    data = {
        "votes": {
            1: 0,
            5: 1
        }
    }

    response = client.post(f'/boxes/{box_id}/vote', json=data, headers=headers)
    assert response.status_code == 400
    assert {"message": "Please vote for all options"} == json.loads(response.data)

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


def test_vote_option_success(client):
    # create header
    token = create_dummy_user(username="mia", password="abc")
    headers = create_headers(token)
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

    response = client.post(f'/boxes/{box_id}/vote', json=data, headers=headers)
    assert response.status_code == 200
    assert {"message": "Vote successfully"} == json.loads(response.data)

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

    response = client.post(f'/boxes/{box_id}/vote', json=data, headers=headers)
    assert response.status_code == 200
    assert {"message": "Vote successfully"} == json.loads(response.data)

    all_votes_after = get_current_votes(box_id)
    expected_all_votes_after = {
        1: [1, 1, 0],
        2: [0, 1, 1],
        3: [1, 1, 0],
        4: [0, 2, 0]
    }
    assert expected_all_votes_after == all_votes_after
