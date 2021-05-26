"""empty message

Revision ID: 20347ca29fe0
Revises: f85ce26c038a
Create Date: 2021-05-18 20:59:25.416342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20347ca29fe0'
down_revision = 'f85ce26c038a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('availible_inventory', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('video', 'availible_inventory')
    # ### end Alembic commands ###
