"""add department

Revision ID: 454f6529bb57
Revises: 16ec81bdf265
Create Date: 2026-04-18
"""

from alembic import op
import sqlalchemy as sa

# 🔥 ОБЯЗАТЕЛЬНО
revision = '454f6529bb57'
down_revision = '16ec81bdf265'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'departments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=True)
    )


def downgrade():
    op.drop_table('departments')