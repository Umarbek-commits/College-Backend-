"""add email to student

Revision ID: 3b4a6586e046
Revises: 454f6529bb57
Create Date: 2026-04-18 06:53:32.409821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b4a6586e046'
down_revision: Union[str, Sequence[str], None] = '454f6529bb57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
