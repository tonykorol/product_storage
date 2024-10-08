"""0003_rename_field_stock

Revision ID: 1620b6362314
Revises: 0e7ef158045b
Create Date: 2024-09-24 12:59:52.490889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1620b6362314'
down_revision: Union[str, None] = '0e7ef158045b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('stock', sa.Integer(), nullable=False))
    op.drop_column('products', 'quantity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('products', 'stock')
    # ### end Alembic commands ###
