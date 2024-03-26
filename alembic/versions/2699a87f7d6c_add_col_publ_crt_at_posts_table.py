"""add col publ crt at posts table

Revision ID: 2699a87f7d6c
Revises: 8059b61fa27f
Create Date: 2024-03-25 04:17:24.034571

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, TIMESTAMP, Boolean, text

# revision identifiers, used by Alembic.
revision: str = '2699a87f7d6c'
down_revision: Union[str, None] = '8059b61fa27f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", Column("published", Boolean, nullable=False, server_default='TRUE'))
    op.add_column("posts", Column("created_at", TIMESTAMP(timezone=True), 
                                  nullable=False, server_default=text("NOW()")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "publish")
    op.drop_column("posts", "created_at")
    pass
