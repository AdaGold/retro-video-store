"""added Rental model v1 and made Fk changes to Customer and Video model

Revision ID: cb7a59bb35d5
Revises: 88621cc911cb
Create Date: 2021-05-19 20:45:54.508759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb7a59bb35d5'
down_revision = '88621cc911cb'
branch_labels = None
depends_on = None


# def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('rental',
    # sa.Column('rental_id', sa.Integer(), nullable=False),
    # sa.Column('due_date', sa.DateTime(), nullable=True),
    # sa.Column('customer_id', sa.Integer(), nullable=True),
    # sa.Column('video_id', sa.Integer(), nullable=True),
    # sa.ForeignKeyConstraint(['customer_id'], ['customer.customer_id'], ),
    # sa.ForeignKeyConstraint(['video_id'], ['video.video_id'], ),
    # sa.PrimaryKeyConstraint('rental_id', 'customer_id', 'video_id')
    # )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rental')
    # ### end Alembic commands ###