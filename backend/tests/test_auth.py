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
            "password": "$argon2id$v=19$m=65536,t=3,p=4$lOKjkmTSzN9E81ulB4VkAA$RQiMP2SfSU4hRtOIxE4ToH4sYT6G0v54fcz024zs27I"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data

    assert data["token_type"] == "bearer"
    