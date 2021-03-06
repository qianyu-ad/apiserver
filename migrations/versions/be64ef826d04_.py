"""empty message

Revision ID: be64ef826d04
Revises: cdc9d536917f
Create Date: 2018-09-14 23:05:30.199910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be64ef826d04'
down_revision = 'cdc9d536917f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('code', sa.String(length=20), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'code')
    # ### end Alembic commands ###
