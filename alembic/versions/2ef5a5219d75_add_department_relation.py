"""add department relation

Revision ID: 2ef5a5219d75
Revises: a013bd6942db
Create Date: 2026-04-18 06:59:09.289060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ef5a5219d75'
down_revision: Union[str, Sequence[str], None] = 'a013bd6942db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
