from sqlalchemy.orm import Session

from app.models.agent import AgentModel
from app.schemas.agent import Agent, AgentRole


class AgentService:
    """Service layer for persistent AI agent management."""

    def __init__(self, db: Session):
        self.db = db

    def create_agent(self, agent: Agent) -> Agent:
        model = AgentModel(
            id=agent.id,
            name=agent.name,
            role=agent.role,
            agent_type=agent.agent_type.value,
            status=agent.status.value if agent.status else "inactive",
            capabilities=agent.capabilities,
            reports_to=agent.reports_to,
            description=agent.description,
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return self._to_schema(model)

    def get_agent(self, agent_id: str) -> Agent | None:
        model = (
            self.db.query(AgentModel)
            .filter(AgentModel.id == agent_id)
            .first()
        )

        if model is None:
            return None

        return self._to_schema(model)

    def list_agents(self) -> list[Agent]:
        models = (
            self.db.query(AgentModel)
            .order_by(AgentModel.created_at)
            .all()
        )

        return [
            self._to_schema(model)
            for model in models
        ]

    def find_by_role(self, role: AgentRole) -> list[Agent]:
        models = (
            self.db.query(AgentModel)
            .filter(AgentModel.role == role.value)
            .order_by(AgentModel.created_at)
            .all()
        )

        return [
            self._to_schema(model)
            for model in models
        ]

    def remove_agent(self, agent_id: str) -> bool:
        model = (
            self.db.query(AgentModel)
            .filter(AgentModel.id == agent_id)
            .first()
        )

        if model is None:
            return False

        self.db.delete(model)
        self.db.commit()

        return True

    @staticmethod
    def _to_schema(model: AgentModel) -> Agent:
        return Agent(
        id=model.id,
        name=model.name,
        role=model.role,
        agent_type=model.agent_type,
        status=model.status,
        capabilities=model.capabilities or [],
        reports_to=model.reports_to,
        description=model.description,
    )
        