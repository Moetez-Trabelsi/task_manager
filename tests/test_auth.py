from fastapi.testclient import TestClient

def test_login_success(client, created_user):
    response=client.post(
        "/auth/login",
        data={
        "username": "test@example.com",
        "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_login_wrong_password(client, created_user):
    response=client.post(
        "/auth/login",
        data={
        "username": "test@example.com",
        "password": "wrong password"
        }
    )
    assert response.status_code == 403

def test_login_nonexistent_user(client, created_user):
    response=client.post(
        "/auth/login",
        data={
        "username": "wrong@example.com",
        "password": "password123"
        }
    )
    assert response.status_code == 403
