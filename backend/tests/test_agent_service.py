from app.schemas.agent import Agent, AgentRole, AgentStatus
from app.services.agent_service import AgentService


def make_agent(agent_id: str, role: AgentRole) -> Agent:
    return Agent(
        id=agent_id,
        name=f"{role.value.title()} Agent",
        role=role,
        description=f"Handles {role.value} tasks.",
        status=AgentStatus.ACTIVE,
    )


def test_create_and_get_agent():
    service = AgentService()

    agent = make_agent(
        "engineering-01",
        AgentRole.ENGINEERING,
    )

    created = service.create_agent(agent)

    assert created == agent
    assert service.get_agent("engineering-01") == agent


def test_list_agents():
    service = AgentService()

    engineering = make_agent(
        "engineering-01",
        AgentRole.ENGINEERING,
    )

    research = make_agent(
        "research-01",
        AgentRole.RESEARCH,
    )

    service.create_agent(engineering)
    service.create_agent(research)

    agents = service.list_agents()

    assert len(agents) == 2
    assert engineering in agents
    assert research in agents


def test_find_agents_by_role():
    service = AgentService()

    engineering = make_agent(
        "engineering-01",
        AgentRole.ENGINEERING,
    )

    research = make_agent(
        "research-01",
        AgentRole.RESEARCH,
    )

    service.create_agent(engineering)
    service.create_agent(research)

    results = service.find_by_role(
        AgentRole.ENGINEERING
    )

    assert len(results) == 1
    assert results[0] == engineering


def test_remove_agent():
    service = AgentService()

    agent = make_agent(
        "engineering-01",
        AgentRole.ENGINEERING,
    )

    service.create_agent(agent)

    assert service.remove_agent("engineering-01") is True
    assert service.get_agent("engineering-01") is None