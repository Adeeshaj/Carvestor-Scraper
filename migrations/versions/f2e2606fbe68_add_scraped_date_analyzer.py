"""add scraped date analyzer

Revision ID: f2e2606fbe68
Revises: e7367a63acc9
Create Date: 2023-11-25 10:17:45.684189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2e2606fbe68'
down_revision: Union[str, None] = 'e7367a63acc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = 'processed_listings'
def upgrade() -> None:
    op.add_column(table, sa.Column('scraped_date', sa.String()))


def downgrade() -> None:
    op.drop_column(table, 'scraped_date')
