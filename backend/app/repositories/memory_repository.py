"""Database repository for AI memories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.memory import Memory


class MemoryRepository:
    """Persist and retrieve AI memories."""

    def create(
        self,
        db: Session,
        *,
        owner_id: str,
        memory_type: str,
        content: str,
    ) -> Memory:

        memory = Memory(
            owner_id=owner_id,
            memory_type=memory_type,
            content=content,
        )

        db.add(memory)
        db.commit()
        db.refresh(memory)

        return memory

    def list_for_owner(
        self,
        db: Session,
        owner_id: str,
    ) -> list[Memory]:

        statement = (
            select(Memory)
            .where(Memory.owner_id == owner_id)
            .order_by(Memory.created_at.desc())
        )

        return list(
            db.scalars(statement).all()
        )