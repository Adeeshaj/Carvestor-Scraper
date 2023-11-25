"""unique listing url

Revision ID: 2af110079ce9
Revises: f2e2606fbe68
Create Date: 2023-11-25 10:59:49.224463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2af110079ce9'
down_revision: Union[str, None] = 'f2e2606fbe68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = 'processed_listings'

def upgrade() -> None:
    op.create_unique_constraint('unique_constraint_listing_url', table, ['listing_url'])



def downgrade() -> None:
    op.drop_constraint('unique_constraint_listing_url', table, type_='unique')

