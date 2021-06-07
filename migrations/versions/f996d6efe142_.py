"""empty message

Revision ID: f996d6efe142
Revises: 9bb7550db773
Create Date: 2021-06-06 20:11:21.805840

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f996d6efe142'
down_revision = '9bb7550db773'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('customer_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('postal_code', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('registered_at', sa.DateTime(), nullable=True),
    sa.Column('videos_checked_out_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('customer_id')
    )
    op.create_table('rentals',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('video_id', sa.Integer(), nullable=False),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['videos.video_id'], ),
    sa.PrimaryKeyConstraint('id', 'customer_id', 'video_id')
    )
    op.drop_table('customer')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('customer_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('postal_code', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('registered_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('videos_checked_out_count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('customer_id', name='customer_pkey')
    )
    op.drop_table('rentals')
    op.drop_table('customers')
    # ### end Alembic commands ###
