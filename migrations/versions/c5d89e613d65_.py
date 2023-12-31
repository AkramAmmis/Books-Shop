"""empty message

Revision ID: c5d89e613d65
Revises: 0ab1e9c06298
Create Date: 2023-12-06 09:17:01.025502

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c5d89e613d65'
down_revision = '0ab1e9c06298'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_column('num')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('num', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
