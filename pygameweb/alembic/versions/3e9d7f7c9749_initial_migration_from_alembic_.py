"""Initial migration from alembic autogeneration

Revision ID: 3e9d7f7c9749
Revises: 
Create Date: 2016-05-04 09:06:58.280952

"""

# revision identifiers, used by Alembic.
revision = '3e9d7f7c9749'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wikicomment')
    op.drop_table('news')
    op.create_index(op.f('ix_tags_project_id'), 'tags', ['project_id'], unique=False)
    op.create_index(op.f('ix_tags_value'), 'tags', ['value'], unique=False)
    op.drop_index('public_tags_project_id0_idx', table_name='tags')
    op.drop_index('public_tags_value1_idx', table_name='tags')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('public_tags_value1_idx', 'tags', ['value'], unique=False)
    op.create_index('public_tags_project_id0_idx', 'tags', ['project_id'], unique=False)
    op.drop_index(op.f('ix_tags_value'), table_name='tags')
    op.drop_index(op.f('ix_tags_project_id'), table_name='tags')
    op.create_table('news',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('datetimeon', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('submit_users_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='news_pkey')
    )
    op.create_table('wikicomment',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('link', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('users_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('datetimeon', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='wikicomment_pkey')
    )
    ### end Alembic commands ###
