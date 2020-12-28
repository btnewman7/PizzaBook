"""Make index for BlogPost

Revision ID: 8f32018ee27b
Revises: c877d9622852
Create Date: 2020-12-26 12:57:58.465210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f32018ee27b'
down_revision = 'c877d9622852'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_blog_post_created_on'), 'blog_post', ['created_on'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_blog_post_created_on'), table_name='blog_post')
    # ### end Alembic commands ###