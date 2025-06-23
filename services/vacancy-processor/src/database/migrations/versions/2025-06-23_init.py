"""init

Revision ID: d753351ee82b
Revises: 
Create Date: 2025-06-23 16:13:17.178389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd753351ee82b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS vacancy_processor")  # added manually


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS vacancy_processor CASCADE")  # added manually
