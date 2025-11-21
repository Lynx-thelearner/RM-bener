"""penambahan atribut

Revision ID: 89fc847b810b
Revises: 18280bcc1080
Create Date: 2025-11-19 15:26:48.740438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89fc847b810b'
down_revision: Union[str, Sequence[str], None] = '18280bcc1080'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Buat tipe ENUM PostgreSQL
    tipe_enum = sa.Enum('family', 'couple', 'private', name='tipe_meja')
    tipe_enum.create(op.get_bind(), checkfirst=True)

    # 2. Tambahkan kolom dengan tipe ENUM tersebut
    op.add_column(
        'meja',
        sa.Column('tipe_meja', tipe_enum, nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Hapus kolom
    op.drop_column('meja', 'tipe_meja')

    # 2. Hapus tipe ENUM PostgreSQL
    tipe_enum = sa.Enum(name='tipe_meja')
    tipe_enum.drop(op.get_bind(), checkfirst=True)
