"""empty message

Revision ID: 9ae63bb6686a
Revises: c737951515fe
Create Date: 2021-05-18 11:30:53.721992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ae63bb6686a'
down_revision = 'c737951515fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('available_inventory', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('video', 'available_inventory')
    # ### end Alembic commands ###
