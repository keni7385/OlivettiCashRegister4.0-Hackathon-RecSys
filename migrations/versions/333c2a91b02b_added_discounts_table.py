"""Added discounts table

Revision ID: 333c2a91b02b
Revises: c89333e964ac
Create Date: 2019-09-28 10:49:47.263957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '333c2a91b02b'
down_revision = 'c89333e964ac'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('discount',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('transaction_id', sa.String(length=64), nullable=True),
                    sa.Column('sku_id', sa.String(length=64), nullable=True),
                    sa.Column('discounted_sku_id', sa.String(length=64), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_sku_id'), 'discount', ['sku_id'], unique=True)
    op.create_index(op.f('ix_discounted_sku_id'), 'discount', ['discounted_sku_id'], unique=True)
    op.create_index(op.f('ix_transaction_id'), 'discount', ['transaction_id'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_transaction_id'), table_name='discount')
    op.drop_index(op.f('ix_discounted_sku_id'), table_name='discount')
    op.drop_index(op.f('ix_sku_id'), table_name='discount')
    op.drop_table('discount')
