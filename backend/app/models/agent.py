"""Database models for Novixa AI agents and persistent agent memory."""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AgentModel(Base):
    """Persistent representation of an AI agent."""

    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    agent_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="employee",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="inactive",
    )

    capabilities: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    reports_to: Mapped[str | None] = mapped_column(
        ForeignKey("agents.id"),
        nullable=True,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class AgentMemoryModel(Base):
    """Persistent memory belonging to an AI agent."""

    __tablename__ = "agent_memories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    agent_id: Mapped[str] = mapped_column(
        ForeignKey("agents.id"),
        nullable=False,
        index=True,
    )

    memory_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    memory_metadata: Mapped[dict] = mapped_column(
    "metadata",
    JSON,
    nullable=False,
    default=dict,
    )

    importance: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.5,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )