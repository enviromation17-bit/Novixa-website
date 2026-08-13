from app.schemas.agent import Agent, AgentRole, AgentStatus
from app.services.agent_registry import AgentRegistry


def make_agent(
    agent_id: str,
    role: AgentRole,
) -> Agent:
    return Agent(
        id=agent_id,
        name=f"{role.value.title()} Agent",
        role=role,
        description=f"Handles {role.value} tasks.",
        status=AgentStatus.ACTIVE,
    )


def test_register_and_get_agent():
    registry = AgentRegistry()
    agent = make_agent("engineering-01", AgentRole.ENGINEERING)

    registered = registry.register(agent)

    assert registered == agent
    assert registry.get("engineering-01") == agent


def test_list_all_agents():
    registry = AgentRegistry()

    engineering = make_agent("engineering-01", AgentRole.ENGINEERING)
    research = make_agent("research-01", AgentRole.RESEARCH)

    registry.register(engineering)
    registry.register(research)

    agents = registry.list_all()

    assert len(agents) == 2
    assert engineering in agents
    assert research in agents


def test_find_agents_by_role():
    registry = AgentRegistry()

    engineering = make_agent("engineering-01", AgentRole.ENGINEERING)
    research = make_agent("research-01", AgentRole.RESEARCH)
    engineering_two = make_agent("engineering-02", AgentRole.ENGINEERING)

    registry.register(engineering)
    registry.register(research)
    registry.register(engineering_two)

    results = registry.find_by_role(AgentRole.ENGINEERING)

    assert len(results) == 2
    assert engineering in results
    assert engineering_two in results
    assert research not in results


def test_remove_agent():
    registry = AgentRegistry()
    agent = make_agent("engineering-01", AgentRole.ENGINEERING)

    registry.register(agent)

    assert registry.remove("engineering-01") is True
    assert registry.get("engineering-01") is None


def test_remove_missing_agent_returns_false():
    registry = AgentRegistry()

    assert registry.remove("does-not-exist") is False