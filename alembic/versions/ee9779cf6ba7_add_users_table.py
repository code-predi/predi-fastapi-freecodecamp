"""add users table

Revision ID: ee9779cf6ba7
Revises: 2584b71bc264
Create Date: 2024-03-25 02:50:36.346796

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, String, TIMESTAMP, text


# revision identifiers, used by Alembic.
revision: str = 'ee9779cf6ba7'
down_revision: Union[str, None] = '2584b71bc264'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", Column(name="id", type_=Integer, nullable=False, primary_key=True),
                    Column(name="email", type_=String, nullable=False, unique=True),
                    Column(name="pasword", type_=String, nullable=False),
                    Column("created_at", TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False),)
    pass

def downgrade() -> None:
    op.drop_table("users")
    pass
