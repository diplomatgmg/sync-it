"""initial

Revision ID: ee7ce470e504
Revises:
Create Date: 2025-06-14 23:17:54.845435

"""
from collections.abc import Sequence

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "ee7ce470e504"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS vacancy_parser")  # added manually


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS vacancy_parser CASCADE")  # added manually
