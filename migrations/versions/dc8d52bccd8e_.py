"""empty message

Revision ID: dc8d52bccd8e
Revises: 4d18a8107290
Create Date: 2019-04-20 20:16:42.943143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc8d52bccd8e'
down_revision = '4d18a8107290'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookmarks', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint(None, 'bookmarks', type_='foreignkey')
    op.create_foreign_key(None, 'bookmarks', 'user', ['user_id'], ['id'])
    op.drop_column('bookmarks', 'user.id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookmarks', sa.Column('user.id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'bookmarks', type_='foreignkey')
    op.create_foreign_key(None, 'bookmarks', 'user', ['user.id'], ['id'])
    op.drop_column('bookmarks', 'user_id')
    # ### end Alembic commands ###
