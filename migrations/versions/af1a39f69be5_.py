"""empty message

Revision ID: af1a39f69be5
Revises: a48766184924
Create Date: 2021-05-21 14:58:28.204057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af1a39f69be5'
down_revision = 'a48766184924'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('total_inventory', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('video', 'total_inventory')
    # ### end Alembic commands ###
