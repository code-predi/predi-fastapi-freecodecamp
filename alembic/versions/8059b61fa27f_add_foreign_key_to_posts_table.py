"""add foreign key to posts table

Revision ID: 8059b61fa27f
Revises: ee9779cf6ba7
Create Date: 2024-03-25 03:49:23.478675

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, String


# revision identifiers, used by Alembic.
revision: str = '8059b61fa27f'
down_revision: Union[str, None] = 'ee9779cf6ba7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", Column("owner_id", Integer, nullable=False))
    op.create_foreign_key(constraint_name="posts_users_fk", source_table="posts", referent_table="users",
                          local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint(constraint_name="posts_users_fk", table_name="posts")
    op.drop_column(table_name="posts", column_name="owner_id")
    pass
