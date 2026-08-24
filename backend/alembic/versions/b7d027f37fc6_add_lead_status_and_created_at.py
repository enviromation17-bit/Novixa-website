"""add lead status and created at

Revision ID: b7d027f37fc6
Revises: 226852d6b3e1
Create Date: 2026-08-09 09:46:05.110643
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b7d027f37fc6"
down_revision: Union[str, Sequence[str], None] = "226852d6b3e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "contacts",
        sa.Column(
            "status",
            sa.String(),
            nullable=False,
            server_default="new",
        ),
    )

    op.add_column(
        "contacts",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True,
        ),
    )

    op.execute(
        "UPDATE contacts "
        "SET created_at = CURRENT_TIMESTAMP "
        "WHERE created_at IS NULL"
    )

    with op.batch_alter_table("contacts") as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),
            nullable=False,
        )

        batch_op.alter_column(
            "status",
            existing_type=sa.String(),
            server_default=None,
        )

        batch_op.create_index(
            "ix_contacts_status",
            ["status"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("contacts") as batch_op:
        batch_op.drop_index("ix_contacts_status")
        batch_op.drop_column("created_at")
        batch_op.drop_column("status")