"""Initial

Revision ID: 03f4c9f74b68
Revises:
Create Date: 2023-10-21 12:51:42.966232

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '03f4c9f74b68'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('urls',
                    sa.Column('token', sa.VARCHAR(length=10), nullable=False),
                    sa.Column('saved_url', sa.TEXT(), nullable=False),
                    sa.PrimaryKeyConstraint('token')
                    )
    op.create_index(op.f('ix_urls_saved_url'), 'urls', ['saved_url'], unique=True)
    op.create_index(op.f('ix_urls_token'), 'urls', ['token'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_urls_token'), table_name='urls')
    op.drop_index(op.f('ix_urls_saved_url'), table_name='urls')
    op.drop_table('urls')
    # ### end Alembic commands ###