"""Initial schema

Revision ID: 25b4f04d5740
Revises: 
Create Date: 2023-10-22 11:23:08.633035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = '25b4f04d5740'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

listings = "listings"

def upgrade() -> None:
    op.create_table(
        listings,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('listing_url', sa.String(), nullable=False),
        sa.Column('title', sa.String()),
        sa.Column('location', sa.String()),
        sa.Column('price', sa.Float()),
        sa.Column('price_currency', sa.String()),
        sa.Column('date', sa.String()),
        sa.Column('properties', JSONB),  # Store properties as a JSONB object
        sa.Column('description', sa.String()),
    )


def downgrade() -> None:
    op.drop_table(table_name)
