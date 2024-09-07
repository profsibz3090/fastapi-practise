"""add foreign key to posts table

Revision ID: ca98af320cf3
Revises: 38be83d57ba1
Create Date: 2024-09-04 18:06:09.254491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca98af320cf3'
down_revision: Union[str, None] = '38be83d57ba1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'])
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    pass
