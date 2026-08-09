from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_contacts_without_token():
    response = client.get("/api/v1/contacts")
    assert response.status_code == 401


def test_get_contacts_with_token():
    login_response = client.post(
        "/api/v1/login",
        json={
            "username": "admin",
            "password": "admin123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/contacts",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
def test_create_contact():
    response = client.post(
        "/api/v1/contacts",
        json={
            "name": "Salman Bari",
            "company": "Novixa",
            "email": "salman@novixa.com",
            "project": "AI Customer Support Agent",
            "message": "We need an AI assistant for our business.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "Thank you" in data["message"]
    assert "id" in data["data"]
def test_create_contact():
    response = client.post(
        "/api/v1/contacts",
        json={
            "name": "Salman Bari",
            "company": "Novixa",
            "email": "salman@novixa.com",
            "project": "AI Customer Support Agent",
            "message": "We need an AI assistant for our business.",
            "status": "new",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "Thank you" in data["message"]
    assert "id" in data["data"]