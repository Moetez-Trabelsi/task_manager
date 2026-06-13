from fastapi.testclient import TestClient

def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "test@example.com", 
            "password": "password123",
            "name": "Test User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data


def test_create_duplicate_user(client, created_user):
    response = client.post(
        "/users/",
        json={"email": "test@example.com", 
            "password": "password123",
            "name": "User Name"
        }
    )
    assert response.status_code == 400

def test_create_user_invalid_email(client):
    response = client.post(
        "/users/",
        json={"email": "notemail", 
            "password": "password123",
            "name": "Test User"
        }
    )
    assert response.status_code == 422

