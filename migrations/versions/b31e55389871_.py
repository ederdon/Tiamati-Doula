"""empty message

Revision ID: b31e55389871
Revises: 72c7fd7d6a5f
Create Date: 2022-06-16 14:44:56.218516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b31e55389871'
down_revision = '72c7fd7d6a5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service', sa.Column('description_short', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('service', 'description_short')
    # ### end Alembic commands ###
