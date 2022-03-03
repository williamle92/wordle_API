"""empty message

Revision ID: c6303c5ac47b
Revises: 054e23d81210
Create Date: 2022-03-02 21:59:35.214548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6303c5ac47b'
down_revision = '054e23d81210'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('attempts', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('game', 'attempts')
    # ### end Alembic commands ###