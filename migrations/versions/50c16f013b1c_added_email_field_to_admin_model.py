"""added email field to admin model

Revision ID: 50c16f013b1c
Revises: 42ddf5ab7241
Create Date: 2020-12-24 20:05:19.855654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50c16f013b1c'
down_revision = '42ddf5ab7241'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admins', sa.Column('email', sa.String(length=120), nullable=True))
    op.create_index(op.f('ix_admins_email'), 'admins', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_admins_email'), table_name='admins')
    op.drop_column('admins', 'email')
    # ### end Alembic commands ###
