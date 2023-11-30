import pytest
from main.main import app

@pytest.fixture
def test_client():
    with app.test_client() as client:
        yield client

def create_user(client, user_data):
    return client.post("/users", json=user_data)

def test_post_user(test_client):
    user_data = {"name": "John", "lastname": "Doe"}
    response = create_user(test_client, user_data)
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["name"] == "John"
    assert response.json["lastname"] == "Doe"

def test_get_user(test_client):
    user_data = {"name": "Alice", "lastname": "Smith"}
    post_response = create_user(test_client, user_data)
    user_id = post_response.json["id"]
    response = test_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json["name"] == "Alice"
    assert response.json["lastname"] == "Smith"

def test_update_user(test_client):
    user_data = {"name": "Bob", "lastname": "Brown"}
    post_response = create_user(test_client, user_data)
    user_id = post_response.json["id"]
    update_data = {"lastname": "Green"}
    response = test_client.patch(f"/users/{user_id}", json=update_data)
    assert response.status_code == 204
    get_response = test_client.get(f"/users/{user_id}")
    assert get_response.json["lastname"] == "Green"

def test_replace_user(test_client):
    user_data = {"name": "Cathy", "lastname": "White"}
    post_response = create_user(test_client, user_data)
    user_id = post_response.json["id"]
    new_data = {"name": "Catherine", "lastname": "Black"}
    response = test_client.put(f"/users/{user_id}", json=new_data)
    assert response.status_code == 204
    get_response = test_client.get(f"/users/{user_id}")
    assert get_response.json["name"] == "Catherine"
    assert get_response.json["lastname"] == "Black"

def test_delete_user(test_client):
    user_data = {"name": "David", "lastname": "Grey"}
    post_response = create_user(test_client, user_data)
    user_id = post_response.json["id"]
    delete_response = test_client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204
    get_response = test_client.get(f"/users/{user_id}")
    assert get_response.status_code == 404

def test_post_user_with_missing_fields(test_client):
    user_data = {"name": "Emily"}
    response = create_user(test_client, user_data)
    assert response.status_code == 400

def test_update_nonexistent_user(test_client):
    update_data = {"lastname": "Green"}
    response = test_client.patch("/users/999", json=update_data)
    assert response.status_code == 400

def test_replace_nonexistent_user(test_client):
    replace_data = {"name": "Nonexistent", "lastname": "User"}
    response = test_client.put("/users/999", json=replace_data)
    assert response.status_code == 400

def test_delete_nonexistent_user(test_client):
    response = test_client.delete("/users/999")
    assert response.status_code == 404
