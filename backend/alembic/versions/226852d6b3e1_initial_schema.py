"""initial schema

Revision ID: 226852d6b3e1
Revises:
Create Date: 2026-08-06 18:25:16.324584
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "226852d6b3e1"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("company", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("project", sa.String(), nullable=True),
        sa.Column("message", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_contacts_id",
        "contacts",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_contacts_id", table_name="contacts")
    op.drop_table("contacts")