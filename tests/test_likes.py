from fastapi.testclient import TestClient

from tests.utils import create_user_and_get_token

def create_post(client: TestClient, headers: dict, title: str = "Test Post"):
    return client.post(
        "/posts/",
        json={"title": title, "content": "Content"},
        headers=headers
    ).json()

def test_like_post(client: TestClient):
    headers = create_user_and_get_token(client)
    post = create_post(client, headers)

    response = client.post(
        "/likes/",
        json={"post_id": post["id"]},
        headers=headers
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Post liked"}

def test_duplicate_like(client: TestClient):
    headers = create_user_and_get_token(client)
    post = create_post(client, headers)

    # First like
    client.post( "/likes/", json={"post_id": post["id"]}, headers=headers )

    # Second like
    response = client.post(
        "/likes/",
        json={"post_id": post["id"]},
        headers=headers
    )
    assert response.status_code == 400
    assert "already liked" in response.json()["detail"]

def test_unlike_post(client: TestClient):
    headers = create_user_and_get_token(client)
    post = create_post(client, headers)

    # Like first
    client.post( "/likes/", json={"post_id": post["id"]}, headers=headers )

    # Unlike
    response = client.request(
        "DELETE",
        "/likes/",
        json={"post_id": post["id"]},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Post unliked"}

def test_unlike_not_liked(client: TestClient):
    headers = create_user_and_get_token(client)
    post = create_post(client, headers)

    response = client.request(
        "DELETE",
        "/likes/",
        json={"post_id": post["id"]},
        headers=headers
    )
    assert response.status_code == 400
    assert "not liked" in response.json()["detail"]

def test_like_non_existent_post(client: TestClient):
    headers = create_user_and_get_token(client)
    response = client.post(
        "/likes/",
        json={"post_id": 99999},
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Post with id 99999 not found"
