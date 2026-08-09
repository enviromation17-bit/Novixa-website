from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_invalid_credentials():
    response = client.post(
        "/api/v1/login",
        json={
            "username": "wrong",
            "password": "wrong"
        }
    )

    assert response.status_code == 401
    
def test_login_success():

    response = client.post(
        "/api/v1/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
        

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data

    assert data["token_type"] == "bearer"
    
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_invalid_credentials():
    response = client.post(
        "/api/v1/login",
        json={
            "username": "wrong",
            "password": "wrong"
        }
    )

    assert response.status_code == 401
    