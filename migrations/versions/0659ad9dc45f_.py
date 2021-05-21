"""empty message

Revision ID: 0659ad9dc45f
Revises: e5b91142f301
Create Date: 2021-05-21 10:38:46.631538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0659ad9dc45f'
down_revision = 'e5b91142f301'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('available_inventory', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('video', 'available_inventory')
    # ### end Alembic commands ###
