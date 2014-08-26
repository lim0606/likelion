"""empty message

Revision ID: 239195fd2cd5
Revises: 48e6791981b6
Create Date: 2014-08-11 20:48:57.971000

"""

# revision identifiers, used by Alembic.
revision = '239195fd2cd5'
down_revision = '48e6791981b6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('like', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'like')
    ### end Alembic commands ###