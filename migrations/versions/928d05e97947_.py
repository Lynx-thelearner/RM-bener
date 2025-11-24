"""empty message

Revision ID: 928d05e97947
Revises: 89fc847b810b
Create Date: 2025-11-21 17:57:41.080250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '928d05e97947'
down_revision: Union[str, Sequence[str], None] = '89fc847b810b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("ALTER TYPE reservationstatus ADD VALUE IF NOT EXISTS 'berlangsung';")



def downgrade() -> None:
    """Downgrade schema."""
    pass
