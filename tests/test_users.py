from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "strongpassword123"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "is_active" in data
    assert "password" not in data  # Security check

def test_create_user_duplicate_email(client: TestClient):
    # First create
    client.post(
        "/users/",
        json={"email": "duplicate@example.com", "password": "strongpassword123"},
    )
    # Second create with same email
    response = client.post(
        "/users/",
        json={"email": "duplicate@example.com", "password": "otherpassword"},
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "User with email duplicate@example.com already exists"

def test_get_user(client: TestClient):
    # Create user first
    res = client.post(
        "/users/",
        json={"email": "getme@example.com", "password": "strongpassword123"},
    )
    user_id = res.json()["id"]

    # Get user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "getme@example.com"
    assert data["id"] == user_id

def test_get_non_existent_user(client: TestClient):
    response = client.get("/users/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User with id 99999 not found"

def test_create_user_invalid_email(client: TestClient):
    response = client.post(
        "/users/",
        json={"email": "notanemail", "password": "strongpassword123"},
    )
    # Pydantic validation error
    assert response.status_code == 422
