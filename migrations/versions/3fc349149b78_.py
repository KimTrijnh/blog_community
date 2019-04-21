"""empty message

Revision ID: 3fc349149b78
Revises: a91662f75c80
Create Date: 2019-04-22 01:14:06.030934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fc349149b78'
down_revision = 'a91662f75c80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bookmarks', type_='foreignkey')
    op.create_foreign_key(None, 'bookmarks', 'user', ['user_id'], ['id'])
    op.drop_column('bookmarks', 'user.id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookmarks', sa.Column('user.id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'bookmarks', type_='foreignkey')
    op.create_foreign_key(None, 'bookmarks', 'user', ['user.id'], ['id'])
    # ### end Alembic commands ###
