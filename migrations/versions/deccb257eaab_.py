"""empty message

Revision ID: deccb257eaab
Revises: 76b2be5cb1bb
Create Date: 2019-04-21 00:29:02.388302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'deccb257eaab'
down_revision = '76b2be5cb1bb'
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
