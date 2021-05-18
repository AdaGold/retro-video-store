"""empty message

Revision ID: 2c7ab440d44a
Revises: 
Create Date: 2021-05-18 09:31:20.679075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c7ab440d44a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('customer_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('postal_code', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('registered_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('customer_id')
    )
    op.create_table('video',
    sa.Column('video_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('release_date', sa.DateTime(), nullable=True),
    sa.Column('total_copies', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('video_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video')
    op.drop_table('customer')
    # ### end Alembic commands ###
