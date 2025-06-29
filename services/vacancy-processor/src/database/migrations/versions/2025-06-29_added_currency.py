"""added currency

Revision ID: 677b79167cfc
Revises: a4395a8b6c1d
Create Date: 2025-06-29 08:33:46.070282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '677b79167cfc'
down_revision: Union[str, Sequence[str], None] = 'a4395a8b6c1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('value'),
    schema='vacancy_processor'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('currency', schema='vacancy_processor')
    # ### end Alembic commands ###
