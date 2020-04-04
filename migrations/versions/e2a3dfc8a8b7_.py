"""empty message

Revision ID: e2a3dfc8a8b7
Revises: 9b693f8eb50d
Create Date: 2020-04-03 23:42:53.262404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2a3dfc8a8b7'
down_revision = '9b693f8eb50d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('runtime', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stats')
    # ### end Alembic commands ###