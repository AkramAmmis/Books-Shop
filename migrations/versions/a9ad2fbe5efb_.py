"""empty message

Revision ID: a9ad2fbe5efb
Revises: 22a46247e1ad
Create Date: 2023-10-01 11:42:55.142432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9ad2fbe5efb'
down_revision = '22a46247e1ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('warenkorb', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_column('warenkorb')

    # ### end Alembic commands ###
