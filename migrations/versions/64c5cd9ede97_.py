"""empty message

Revision ID: 64c5cd9ede97
Revises: b05d356241c7
Create Date: 2023-09-16 10:30:11.577253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64c5cd9ede97'
down_revision = 'b05d356241c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'user', ['author'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('author')

    # ### end Alembic commands ###
