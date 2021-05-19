"""empty message

Revision ID: 94497a0ad968
Revises: c2b5a7267f6e
Create Date: 2021-05-19 10:58:41.553819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94497a0ad968'
down_revision = 'c2b5a7267f6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rentals')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rentals',
    sa.Column('customer_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('video_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], name='rentals_customer_id_fkey'),
    sa.ForeignKeyConstraint(['video_id'], ['video.id'], name='rentals_video_id_fkey')
    )
    # ### end Alembic commands ###
