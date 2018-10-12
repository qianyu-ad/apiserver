"""empty message

Revision ID: ef963f9f99f7
Revises: 8a5510bfb9c8
Create Date: 2018-10-13 00:35:51.452674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef963f9f99f7'
down_revision = '8a5510bfb9c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('index', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'index')
    # ### end Alembic commands ###
