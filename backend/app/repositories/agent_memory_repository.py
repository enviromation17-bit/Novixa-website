"""Repository for persistent AI agent memory."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agent import AgentMemoryModel


class AgentMemoryRepository:
    """Store and retrieve persistent agent memories."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        agent_id: str,
        memory_type: str,
        content: str,
        metadata: dict | None = None,
        importance: float = 0.5,
    ) -> AgentMemoryModel:

        memory = AgentMemoryModel(
            agent_id=agent_id,
            memory_type=memory_type,
            content=content,
            metadata=metadata or {},
            importance=importance,
        )

        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)

        return memory

    def list_for_agent(
        self,
        agent_id: str,
        limit: int = 20,
    ) -> list[AgentMemoryModel]:

        statement = (
            select(AgentMemoryModel)
            .where(AgentMemoryModel.agent_id == agent_id)
            .order_by(
                AgentMemoryModel.importance.desc(),
                AgentMemoryModel.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement).all()
        )