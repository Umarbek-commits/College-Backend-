"""add email to student

Revision ID: a013bd6942db
Revises: 406fffe020a9
Create Date: 2026-04-18 06:55:29.576162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a013bd6942db'
down_revision: Union[str, Sequence[str], None] = '406fffe020a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
