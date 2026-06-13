from fastapi.testclient import TestClient

def test_create_task(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response=client.post(
        "/tasks/",
        json={
        "title": "test_title",
        "description": "test"
        },
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "test_title"
    assert data["description"] == "test"
    assert data["is_completed"] == False
    assert "owner_id" in data
    assert "created_at" in data
    

def test_get_tasks(client, auth_token, created_task):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response=client.get(
        "/tasks/",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "test_title"

def test_get_task_not_found(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response=client.get(
        "/tasks/999",
        headers=headers
    )
    assert response.status_code == 404

def test_update_task(client, auth_token, created_task):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response=client.put(
        f"/tasks/{created_task["id"]}",
        json={
        "title": "updated_test_title",
        "description": "updated_test",
        "is_completed" : True
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "updated_test_title"
    assert data["description"] == "updated_test"
    assert data["is_completed"] == True

def test_delete_task(client, auth_token, created_task):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response=client.delete(
        f"/tasks/{created_task["id"]}",
        headers=headers
    )
    assert response.status_code == 200

def test_unauthorized_access(client):
    response = client.get("/tasks/", )
    assert response.status_code == 401