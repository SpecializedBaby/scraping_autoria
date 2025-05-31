"""add images_count Column

Revision ID: 62f78f6634e8
Revises: 
Create Date: 2025-05-31 11:50:46.457249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62f78f6634e8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('cars', sa.Column('images_count', sa.Integer()))


def downgrade() -> None:
    op.drop_column('cars', 'images_count')
