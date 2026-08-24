from sqlalchemy.orm import Session

from app.models.agent import AgentMemoryModel
from app.schemas.agent_memory import AgentMemory, AgentMemoryCreate


class AgentMemoryService:
    """Persistent memory management for AI agents."""

    def __init__(self, db: Session):
        self.db = db

    def create_memory(
        self,
        agent_id: str,
        memory: AgentMemoryCreate,
    ) -> AgentMemory:
        model = AgentMemoryModel(
            agent_id=agent_id,
            memory_type=memory.memory_type,
            content=memory.content,
            memory_metadata=memory.memory_metadata,
            importance=memory.importance,
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return self._to_schema(model)

    def list_memories(
        self,
        agent_id: str,
    ) -> list[AgentMemory]:
        models = (
            self.db.query(AgentMemoryModel)
            .filter(AgentMemoryModel.agent_id == agent_id)
            .order_by(AgentMemoryModel.created_at)
            .all()
        )

        return [self._to_schema(model) for model in models]

    @staticmethod
    def _to_schema(model: AgentMemoryModel) -> AgentMemory:
        return AgentMemory(
            id=model.id,
            agent_id=model.agent_id,
            memory_type=model.memory_type,
            content=model.content,
            memory_metadata=model.memory_metadata or {},
            importance=model.importance,
            created_at=model.created_at,
        )