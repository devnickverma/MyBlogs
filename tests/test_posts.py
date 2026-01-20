from fastapi.testclient import TestClient

from tests.utils import create_user_and_get_token

def test_create_post(client: TestClient):
    headers = create_user_and_get_token(client)
    response = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "This is a test post."},
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test post."
    assert "id" in data
    assert "created_at" in data

def test_get_post(client: TestClient):
    headers = create_user_and_get_token(client)
    # Create post
    create_res = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "Content"},
        headers=headers
    )
    post_id = create_res.json()["id"]

    # Get post (public)
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["id"] == post_id

def test_get_non_existent_post(client: TestClient):
    response = client.get("/posts/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Post with id 99999 not found"

def test_read_posts(client: TestClient):
    headers = create_user_and_get_token(client)
    # Create valid posts
    client.post(
        "/posts/",
        json={"title": "Post 1", "content": "Content 1"},
        headers=headers
    )
    client.post(
        "/posts/",
        json={"title": "Post 2", "content": "Content 2"},
        headers=headers
    )

    response = client.get("/posts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Verify order: newest first (Post 2 should be first)
    assert data[0]["title"] == "Post 2"
    assert data[1]["title"] == "Post 1"

def test_create_post_invalid(client: TestClient):
    headers = create_user_and_get_token(client)
    response = client.post(
        "/posts/",
        json={"title": "", "content": "Content"},
        headers=headers
    )
    assert response.status_code == 422
