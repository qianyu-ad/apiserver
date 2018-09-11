"""empty message

Revision ID: 93a3572fe986
Revises: a87c647e28c3
Create Date: 2018-09-11 23:25:17.649673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93a3572fe986'
down_revision = 'a87c647e28c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('seo',
    sa.Column('id', sa.String(length=16), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('keywords', sa.Text(), nullable=True),
    sa.Column('desc', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    mysql_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('seo')
    # ### end Alembic commands ###
