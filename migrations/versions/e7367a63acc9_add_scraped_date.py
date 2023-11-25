"""add scraped date

Revision ID: e7367a63acc9
Revises: ed3f724db9db
Create Date: 2023-11-25 09:42:06.224912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7367a63acc9'
down_revision: Union[str, None] = 'ed3f724db9db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

listings = "listings"

def upgrade() -> None:
    op.add_column(listings, sa.Column('scraped_date', sa.String()))



def downgrade() -> None:
    op.drop_column(listings, 'scraped_date')
