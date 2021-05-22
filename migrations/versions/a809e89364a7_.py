"""empty message

Revision ID: a809e89364a7
Revises: 24d1f074f1d1
Create Date: 2021-05-21 12:45:32.410476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a809e89364a7'
down_revision = '24d1f074f1d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rental', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rental', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
