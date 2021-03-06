"""empty message

Revision ID: 73416a8cff96
Revises: 083a0832d011
Create Date: 2021-01-23 00:56:59.864475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73416a8cff96'
down_revision = '083a0832d011'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meals', sa.Column('category', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'meals', 'categories', ['category'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'meals', type_='foreignkey')
    op.drop_column('meals', 'category')
    # ### end Alembic commands ###
