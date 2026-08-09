from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_services():
    response = client.get("/api/v1/services")

    assert response.status_code == 200

    data = response.json()

    assert "services" in data
    assert len(data["services"]) == 4

    assert data["services"][0]["title"] == "AI Engineering"
    assert data["services"][1]["title"] == "Custom Software Development"
    assert data["services"][2]["title"] == "Intelligent Automation"
    assert data["services"][3]["title"] == "Data Intelligence & Analytics"