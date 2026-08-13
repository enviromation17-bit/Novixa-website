from app.schemas.agent import Agent, AgentStatus, AgentType
from app.schemas.agent_task import AgentTask, TaskPriority, TaskStatus


def test_create_ai_ceo():
    agent = Agent(
        id="agent-ceo",
        name="Novixa AI CEO",
        role="Executive Coordinator",
        agent_type=AgentType.CEO,
        capabilities=["delegation", "reporting"],
    )

    assert agent.agent_type == AgentType.CEO
    assert agent.status == AgentStatus.ACTIVE
    assert agent.reports_to is None


def test_create_ai_employee():
    agent = Agent(
        id="agent-engineering",
        name="Engineering Agent",
        role="Software Engineering",
        agent_type=AgentType.EMPLOYEE,
        capabilities=["coding", "testing"],
        reports_to="agent-ceo",
    )

    assert agent.agent_type == AgentType.EMPLOYEE
    assert agent.reports_to == "agent-ceo"


def test_create_agent_task():
    task = AgentTask(
        id="task-001",
        title="Run backend tests",
        description="Execute the backend test suite and report the result.",
        assigned_by="agent-ceo",
        assigned_to="agent-engineering",
        priority=TaskPriority.HIGH,
    )

    assert task.status == TaskStatus.PENDING
    assert task.priority == TaskPriority.HIGH
    assert task.result is None


def test_task_can_complete():
    task = AgentTask(
        id="task-002",
        title="Test task",
        description="A test task.",
        assigned_by="agent-ceo",
        assigned_to="agent-engineering",
        status=TaskStatus.COMPLETED,
        result="22 tests passed",
    )

    assert task.status == TaskStatus.COMPLETED
    assert task.result == "22 tests passed"
