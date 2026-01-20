from fastapi.testclient import TestClient

from tests.utils import create_user_and_get_token

def create_post(client: TestClient, headers: dict, title: str = "Test Post"):
    return client.post(
        "/posts/",
        json={"title": title, "content": "Content"},
        headers=headers
    ).json()

def test_create_comment(client: TestClient):
    headers = create_user_and_get_token(client)
    post = create_post(client, headers)

    response = client.post(
        "/comments",
        json={"content": "This is a comment", "post_id": post["id"]},
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "This is a comment"
    assert data["post_id"] == post["id"]
    assert "id" in data

def test_get_comments_by_post(client: TestClient):
    headers = create_user_and_get_token(client)
    post = create_post(client, headers)
    
    # Create comments
    client.post(
        "/comments",
        json={"content": "Comment 1", "post_id": post["id"]},
        headers=headers
    )
    client.post(
        "/comments",
        json={"content": "Comment 2", "post_id": post["id"]},
        headers=headers
    )

    response = client.get(f"/posts/{post['id']}/comments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["content"] == "Comment 1"
    assert data[1]["content"] == "Comment 2"

def test_create_comment_invalid_post(client: TestClient):
    headers = create_user_and_get_token(client)
    response = client.post(
        "/comments",
        json={"content": "Comment", "post_id": 99999},
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Post with id 99999 not found"

def test_create_comment_invalid_payload(client: TestClient):
    headers = create_user_and_get_token(client)
    post = create_post(client, headers)
    response = client.post(
        "/comments",
        json={"content": "", "post_id": post["id"]},
        headers=headers
    )
    assert response.status_code == 422
