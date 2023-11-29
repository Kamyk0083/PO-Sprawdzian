import pytest
from main import app

@pytest.fixture
def test_client():
    with app.test_client() as client:
        yield client

def test_ping(test_client):
    response = test_client.get("/ping")
    assert response.data == b"ping"

def test_get_users_empty(test_client):
    response = test_client.get("/users")
    assert response.status_code == 200
    assert response.json == []

def test_post_user(test_client):
    user_data = {"name": "John", "lastname": "Doe"}
    response = test_client.post("/users", json=user_data)
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["name"] == "John"
    assert response.json["lastname"] == "Doe"

def test_get_user(test_client):
    user_data = {"name": "Alice", "lastname": "Smith"}
    post_response = test_client.post("/users", json=user_data)
    user_id = post_response.json["id"]
    response = test_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json["name"] == "Alice"
    assert response.json["lastname"] == "Smith"

def test_update_user(test_client):
    user_data = {"name": "Bob", "lastname": "Brown"}
    post_response = test_client.post("/users", json=user_data)
    user_id = post_response.json["id"]
    update_data = {"lastname": "Green"}
    response = test_client.patch(f"/users/{user_id}", json=update_data)
    assert response.status_code == 204
    response = test_client.get(f"/users/{user_id}")
    assert response.json["lastname"] == "Green"

def test_replace_user(test_client):
    user_data = {"name": "Cathy", "lastname": "White"}
    post_response = test_client.post("/users", json=user_data)
    user_id = post_response.json["id"]
    new_data = {"name": "Catherine", "lastname": "Black"}
    response = test_client.put(f"/users/{user_id}", json=new_data)
    assert response.status_code == 204
    response = test_client.get(f"/users/{user_id}")
    assert response.json["name"] == "Catherine"
    assert response.json["lastname"] == "Black"

def test_delete_user(test_client):
    user_data = {"name": "David", "lastname": "Grey"}
    post_response = test_client.post("/users", json=user_data)
    user_id = post_response.json["id"]
    response = test_client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    response = test_client.get(f"/users/{user_id}")
    assert response.status_code == 404
