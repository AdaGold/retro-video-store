"""empty message

Revision ID: e699e09cabc8
Revises: f5d5abfe9db7
Create Date: 2021-05-18 14:09:07.416964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e699e09cabc8'
down_revision = 'f5d5abfe9db7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('videos_checked_out_count', sa.Integer(), nullable=True))
    op.drop_column('customer', 'videos_checked_out')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('videos_checked_out', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('customer', 'videos_checked_out_count')
    # ### end Alembic commands ###
