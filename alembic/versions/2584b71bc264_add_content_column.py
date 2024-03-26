"""add content column

Revision ID: 2584b71bc264
Revises: 1eece279f10c
Create Date: 2024-03-25 02:41:53.206395

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, String


# revision identifiers, used by Alembic.
revision: str = '2584b71bc264'
down_revision: Union[str, None] = '1eece279f10c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", Column(name="content", type_=Integer, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column(table_name="posts", column_name="content")
    pass
