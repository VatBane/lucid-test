"""initial

Revision ID: 05408a9ee825
Revises: 
Create Date: 2025-03-14 19:44:09.760341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '05408a9ee825'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(length=128), nullable=False),
                    sa.Column('password', sa.Text(), nullable=False),
                    sa.PrimaryKeyConstraint('id', name='user_pkey'),
                    sa.UniqueConstraint('email', name='user_email_uc')
                    )
    op.create_table('post',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('text', sa.Text(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='post_user_fkey', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name='post_pkey')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.drop_table('user')
    # ### end Alembic commands ###
