"""create category table

Revision ID: 630b3c4ace28
Revises: 
Create Date: 2025-07-22 10:06:10.891222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '630b3c4ace28'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'category',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255)),
        sa.Column('slug', sa.String(255)),
    )


def downgrade() -> None:
    op.drop_table('category')
