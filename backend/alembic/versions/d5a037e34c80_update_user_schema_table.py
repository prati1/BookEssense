"""update user schema table

Revision ID: d5a037e34c80
Revises: 
Create Date: 2024-07-09 21:13:42.213486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5a037e34c80'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('google_auth', sa.Boolean, default=True))

def downgrade() -> None:
    op.drop_column('users', 'google_auth')
