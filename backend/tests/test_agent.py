from app.schemas.agent import Agent, AgentRole, AgentStatus


def test_agent_defaults_to_inactive():
    agent = Agent(
        id="engineering-01",
        name="Engineering Agent",
        role=AgentRole.ENGINEERING,
        description="Handles software engineering tasks.",
    )

    assert agent.status == AgentStatus.INACTIVE
    assert agent.capabilities == []


def test_agent_accepts_capabilities():
    agent = Agent(
        id="research-01",
        name="Research Agent",
        role=AgentRole.RESEARCH,
        description="Researches information and produces findings.",
        status=AgentStatus.ACTIVE,
        capabilities=["web_research", "summarization"],
    )

    assert agent.status == AgentStatus.ACTIVE
    assert "web_research" in agent.capabilities


def test_agent_role_is_restricted():
    agent = Agent(
        id="automation-01",
        name="Automation Agent",
        role=AgentRole.AUTOMATION,
        description="Handles automation workflows.",
    )

    assert agent.role == AgentRole.AUTOMATION