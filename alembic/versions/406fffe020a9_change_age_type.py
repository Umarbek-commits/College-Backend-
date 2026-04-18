"""change age type

Revision ID: 406fffe020a9
Revises: 3b4a6586e046
Create Date: 2026-04-18 06:54:06.555289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '406fffe020a9'
down_revision: Union[str, Sequence[str], None] = '3b4a6586e046'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
