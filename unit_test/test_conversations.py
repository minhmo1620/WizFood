import json

from unit_test.helpers import create_headers, create_dummy_user_with_knowledgeBase, \
    get_all_conversations, get_latest_conversation

PATH = 'app.controllers.conversations.execute_models'

def test_create_new_conversation(client, mocker):
    token, user_id = create_dummy_user_with_knowledgeBase("test1", "password1")
    headers = create_headers(token)

    # Unauthorized
    response = client.post("/conversations")
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Authorization required"}

    # Before creating new conversation
    pre_add_conversations = get_all_conversations(user_id)

    # Valid request
    mocker.patch(PATH, return_value = json.dumps({
        "message": "What is your preference food cuisine today?", 
        "options": ["asian", "eastern", "western"]
    }))

    response = client.post("/conversations", headers=headers)
    assert response.status_code == 201
    assert json.loads(response.data) == {
        "message": "What is your preference food cuisine today?", 
        "options": ["asian", "eastern", "western"]
    }
    post_add_conversations = get_all_conversations(user_id)

    assert (len(post_add_conversations) - len(pre_add_conversations)) == 1

def test_update_conversation(client, mocker):
    token, user_id = create_dummy_user_with_knowledgeBase("test1", "password1")
    headers = create_headers(token)

    # Create new conversation
    mocker.patch(PATH, return_value = json.dumps({
        "message": "What is your preference food cuisine today?", 
        "options": ["asian", "eastern", "western"]
    }))

    client.post("/conversations", headers=headers)
    conversation = get_latest_conversation(user_id)
    assert json.loads(conversation.answers) == []

    # Update conversation - Fail
    expected_response_model = "Error: Some issues"
    mocker.patch(PATH, return_value = expected_response_model)

    data = {
        "answer": "asian"
    }
    response = client.put("/conversations", headers=headers, json=data)
    assert response.status_code == 400
    assert json.loads(response.data) == {'message': expected_response_model}

    # Check the data to make sure we added new answer
    conversation = get_latest_conversation(user_id)
    assert json.loads(conversation.answers) == []

    # Update conversation - Pass
    expected_response_model = json.dumps({
        "message": "Do you want to have food with rice today?", 
        "options": ["yes", "no"]
    })
    mocker.patch(PATH, return_value = expected_response_model)

    data = {
        "answer": "asian"
    }
    response = client.put("/conversations", headers=headers, json=data)
    assert response.status_code == 200
    assert json.loads(response.data) == json.loads(expected_response_model)

    # Check the data to make sure we added new answer
    conversation = get_latest_conversation(user_id)
    assert json.loads(conversation.answers) == ["asian"]
