from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_agent():
    response = client.post(
        "/api/v1/agents",
        json={
            "id": "api-engineering-01",
            "name": "Engineering Agent",
            "role": "engineering",
            "agent_type": "employee",
            "status": "active",
            "capabilities": ["coding", "testing"],
            "reports_to": "agent-ceo",
            "description": "Handles software engineering tasks.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "api-engineering-01"
    assert data["name"] == "Engineering Agent"
    assert data["agent_type"] == "employee"


def test_get_agent():
    response = client.get(
        "/api/v1/agents/api-engineering-01"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "api-engineering-01"


def test_list_agents():
    response = client.get("/api/v1/agents")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


def test_find_agents_by_role():
    response = client.get(
        "/api/v1/agents/role/engineering"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert any(
        agent["id"] == "api-engineering-01"
        for agent in data
    )


def test_get_missing_agent():
    response = client.get(
        "/api/v1/agents/does-not-exist"
    )

    assert response.status_code == 404


def test_remove_agent():
    response = client.delete(
        "/api/v1/agents/api-engineering-01"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True


def test_remove_missing_agent():
    response = client.delete(
        "/api/v1/agents/does-not-exist"
    )

    assert response.status_code == 404