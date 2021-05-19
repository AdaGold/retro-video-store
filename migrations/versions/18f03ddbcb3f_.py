"""empty message

Revision ID: 18f03ddbcb3f
Revises: 
Create Date: 2021-05-18 14:55:08.945246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18f03ddbcb3f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('customer_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('postal_code', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('register_at', sa.DateTime(), nullable=True),
    sa.Column('videos_checked_out_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('customer_id')
    )
    op.create_table('video',
    sa.Column('video_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('release_date', sa.DateTime(), nullable=True),
    sa.Column('total_inventory', sa.Integer(), nullable=True),
    sa.Column('available_inventory', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('video_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video')
    op.drop_table('customer')
    # ### end Alembic commands ###
