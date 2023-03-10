"""empty message

Revision ID: 167da1d4f904
Revises: 
Create Date: 2023-02-01 21:46:20.658340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '167da1d4f904'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('warehouses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('city', sa.String(length=80), nullable=False),
    sa.Column('state', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('retail_price', sa.Float(precision=2), nullable=False),
    sa.Column('wholesale_price', sa.Float(precision=2), nullable=False),
    sa.Column('category', sa.String(length=80), nullable=False),
    sa.Column('vendor', sa.String(length=80), nullable=False),
    sa.Column('warehouse_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('warehouse_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('items_tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items_tags')
    op.drop_table('tags')
    op.drop_table('items')
    op.drop_table('warehouses')
    op.drop_table('users')
    # ### end Alembic commands ###
