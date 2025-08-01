"""added models

Revision ID: 5e788f22fc16
Revises: 2843301e18c5
Create Date: 2025-06-30 16:22:19.283117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e788f22fc16'
down_revision: Union[str, Sequence[str], None] = '2843301e18c5'
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
    op.create_table('grade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='vacancy_processor'
    )
    op.create_table('profession',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='vacancy_processor'
    )
    op.create_table('skill_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='vacancy_processor'
    )
    op.create_table('work_format',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='vacancy_processor'
    )
    op.create_table('skill',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['vacancy_processor.skill_category.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='vacancy_processor'
    )
    op.create_table('vacancy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hash', sa.String(length=32), nullable=False),
    sa.Column('link', sa.String(length=256), nullable=False),
    sa.Column('profession_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['profession_id'], ['vacancy_processor.profession.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hash'),
    sa.UniqueConstraint('link'),
    schema='vacancy_processor'
    )
    op.create_table('vacancy_grade',
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.Column('grade_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['grade_id'], ['vacancy_processor.grade.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancy_processor.vacancy.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('vacancy_id', 'grade_id'),
    schema='vacancy_processor'
    )
    op.create_table('vacancy_skill',
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.Column('skill_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['skill_id'], ['vacancy_processor.skill.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancy_processor.vacancy.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('vacancy_id', 'skill_id'),
    schema='vacancy_processor'
    )
    op.create_table('vacancy_work_format',
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.Column('work_format_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancy_processor.vacancy.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['work_format_id'], ['vacancy_processor.work_format.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('vacancy_id', 'work_format_id'),
    schema='vacancy_processor'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vacancy_work_format', schema='vacancy_processor')
    op.drop_table('vacancy_skill', schema='vacancy_processor')
    op.drop_table('vacancy_grade', schema='vacancy_processor')
    op.drop_table('vacancy', schema='vacancy_processor')
    op.drop_table('skill', schema='vacancy_processor')
    op.drop_table('work_format', schema='vacancy_processor')
    op.drop_table('skill_category', schema='vacancy_processor')
    op.drop_table('profession', schema='vacancy_processor')
    op.drop_table('grade', schema='vacancy_processor')
    op.drop_table('currency', schema='vacancy_processor')
    # ### end Alembic commands ###
