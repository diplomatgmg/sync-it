"""init

Revision ID: 0d01a329e26b
Revises: 
Create Date: 2025-06-20 11:51:53.069909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d01a329e26b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS vacancy_parser")  # added manually


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS vacancy_parser CASCADE")  # added manually
