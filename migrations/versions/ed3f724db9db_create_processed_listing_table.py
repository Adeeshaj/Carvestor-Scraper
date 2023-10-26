"""Create Processed Listing Table

Revision ID: ed3f724db9db
Revises: 25b4f04d5740
Create Date: 2023-10-26 21:02:23.902898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ed3f724db9db'
down_revision: Union[str, None] = '25b4f04d5740'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('processed_listings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('listing_url', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('price_currency', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('brand', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('model', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('mileage', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('body_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('condition', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('fuel_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('transmission', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('engine_capacity', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('year_of_manufacture', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('trim_edition', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('listing_date', sa.VARCHAR(), autoincrement=False, nullable=True),

    sa.PrimaryKeyConstraint('id', name='processed_listings_pkey')
    )



def downgrade() -> None:
    op.drop_table('processed_listings')
