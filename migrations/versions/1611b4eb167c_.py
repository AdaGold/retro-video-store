"""empty message

Revision ID: 1611b4eb167c
Revises: 72df6beeb268
Create Date: 2021-05-21 15:06:07.045753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1611b4eb167c'
down_revision = '72df6beeb268'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rental', sa.Column('check_in', sa.DateTime(), nullable=True))
    op.add_column('rental', sa.Column('check_out', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rental', 'check_out')
    op.drop_column('rental', 'check_in')
    # ### end Alembic commands ###
