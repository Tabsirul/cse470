"""merge migrations

Revision ID: feb943d6aac5
Revises: 05c83679745b, 65a2380fe621
Create Date: 2026-11-07 20:06:06.066960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'feb943d6aac5'
down_revision: Union[str, Sequence[str], None] = ('05c83679745b', '65a2380fe621')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
