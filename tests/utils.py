from fastapi.testclient import TestClient

def create_user_and_get_token(client: TestClient, email: str = "test@example.com", password: str = "password123"):
    # Create user
    client.post(
        "/users/",
        json={"email": email, "password": password},
    )
    
    # Login
    response = client.post(
        "/token",
        data={"username": email, "password": password},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
