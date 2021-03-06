"""empty message

Revision ID: 766dfc82cfb4
Revises: 
Create Date: 2020-04-19 11:28:03.209050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '766dfc82cfb4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coffee', sa.Column('description', sa.String(length=400), nullable=True))
    op.add_column('coffee', sa.Column('name', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('coffee', 'name')
    op.drop_column('coffee', 'description')
    # ### end Alembic commands ###
