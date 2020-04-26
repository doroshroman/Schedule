"""empty message

Revision ID: 5251e342f317
Revises: 68bacc05d799
Create Date: 2020-04-26 12:25:24.921116

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5251e342f317'
down_revision = '68bacc05d799'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('FK_GROUP_idx', table_name='lessons')
    op.drop_index('FK_SUBJECT_idx', table_name='lessons')
    op.drop_index('FK_TEACHER_idx', table_name='lessons')
    op.alter_column('subjects', 'subj_type',
               existing_type=mysql.VARCHAR(collation='utf8_unicode_ci', length=45),
               nullable=True)
    op.alter_column('subjects', 'title',
               existing_type=mysql.VARCHAR(collation='utf8_unicode_ci', length=255),
               nullable=True)
    op.alter_column('teachers', 'name',
               existing_type=mysql.VARCHAR(collation='utf8_unicode_ci', length=45),
               nullable=True)
    op.alter_column('teachers', 'patronymic',
               existing_type=mysql.VARCHAR(collation='utf8_unicode_ci', length=45),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('teachers', 'patronymic',
               existing_type=mysql.VARCHAR(collation='utf8_unicode_ci', length=45),
               nullable=False)
    op.alter_column('teachers', 'name',
               existing_type=mysql.VARCHAR(collation='utf8_unicode_ci', length=45),
               nullable=False)
    op.alter_column('subjects', 'title',
               existing_type=mysql.VARCHAR(collation='utf8_unicode_ci', length=255),
               nullable=False)
    op.alter_column('subjects', 'subj_type',
               existing_type=mysql.VARCHAR(collation='utf8_unicode_ci', length=45),
               nullable=False)
    op.create_index('FK_TEACHER_idx', 'lessons', ['teacher_id'], unique=False)
    op.create_index('FK_SUBJECT_idx', 'lessons', ['subject_id'], unique=False)
    op.create_index('FK_GROUP_idx', 'lessons', ['group_id'], unique=False)
    # ### end Alembic commands ###
