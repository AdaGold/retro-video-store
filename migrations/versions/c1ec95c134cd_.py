"""empty message

Revision ID: c1ec95c134cd
Revises: 7418a2d6e9eb
Create Date: 2021-05-17 18:44:11.242317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1ec95c134cd'
down_revision = '7418a2d6e9eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer_video_join',
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('video_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.customer_id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['video.video_id'], ),
    sa.PrimaryKeyConstraint('customer_id', 'video_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('customer_video_join')
    # ### end Alembic commands ###
