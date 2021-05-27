"""empty message

Revision ID: 71d19c0fa8a0
Revises: 7ba36a9c4642
Create Date: 2021-05-20 22:38:36.404048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71d19c0fa8a0'
down_revision = '7ba36a9c4642'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('available_inventory', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('video', 'available_inventory')
    # ### end Alembic commands ###
