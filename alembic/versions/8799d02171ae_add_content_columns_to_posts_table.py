"""add content columns to posts table

Revision ID: 8799d02171ae
Revises: d82254d2b83c
Create Date: 2024-09-04 17:10:36.404477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8799d02171ae'
down_revision: Union[str, None] = 'd82254d2b83c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("content",sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
