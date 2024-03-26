"""create_posts_table

Revision ID: 1eece279f10c
Revises: 
Create Date: 2024-03-21 04:15:39.960531

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, String


# revision identifiers, used by Alembic.
revision: str = '1eece279f10c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", Column("id", Integer, nullable=False, primary_key=True),
                    Column("title", String, nullable=False),)
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
