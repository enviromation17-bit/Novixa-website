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
    