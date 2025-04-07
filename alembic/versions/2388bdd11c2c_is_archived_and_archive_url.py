"""is_archived and archive_url

Revision ID: 2388bdd11c2c
Revises: ba25644d1151
Create Date: 2025-04-07 18:58:24.808804

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2388bdd11c2c'
down_revision: Union[str, None] = 'ba25644d1151'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('is_archived', sa.Boolean(), nullable=True))
    op.add_column('posts', sa.Column('archive_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'archive_url')
    op.drop_column('posts', 'is_archived')
    # ### end Alembic commands ###
