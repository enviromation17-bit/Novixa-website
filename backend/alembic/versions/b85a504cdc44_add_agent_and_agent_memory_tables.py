"""add agent and agent memory tables

Revision ID: b85a504cdc44
Revises: b7d027f37fc6
Create Date: 2026-08-22 12:11:51.973477
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b85a504cdc44"
down_revision: Union[str, Sequence[str], None] = "b7d027f37fc6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "agents",
        sa.Column("id", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("role", sa.String(length=100), nullable=False),
        sa.Column(
            "agent_type",
            sa.String(length=30),
            nullable=False,
            server_default="employee",
        ),
        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
            server_default="inactive",
        ),
        sa.Column(
            "capabilities",
            sa.JSON(),
            nullable=False,
        ),
        sa.Column("reports_to", sa.String(length=100), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["reports_to"],
            ["agents.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_agents_reports_to",
        "agents",
        ["reports_to"],
        unique=False,
    )

    op.create_table(
        "agent_memories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("agent_id", sa.String(length=100), nullable=False),
        sa.Column("memory_type", sa.String(length=50), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column(
            "importance",
            sa.Float(),
            nullable=False,
            server_default="0.5",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["agent_id"],
            ["agents.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_agent_memories_agent_id",
        "agent_memories",
        ["agent_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_agent_memories_agent_id",
        table_name="agent_memories",
    )

    op.drop_table("agent_memories")

    op.drop_index(
        "ix_agents_reports_to",
        table_name="agents",
    )

    op.drop_table("agents")