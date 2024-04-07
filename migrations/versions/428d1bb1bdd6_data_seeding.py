"""data_seeding

Revision ID: 428d1bb1bdd6
Revises: 344a2bb084ed
Create Date: 2024-04-07 11:14:43.050776

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "428d1bb1bdd6"
down_revision: Union[str, None] = "344a2bb084ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute(
        """
        INSERT INTO categories (name, type)
        VALUES
            ('Продукты', 'income'),
            ('Продукты', 'expense'),
            ('Кафе', 'income'),
            ('Кафе', 'expense'),
            ('Налоги', 'income'),
            ('Налоги', 'expense')
        """
    )


def downgrade() -> None:
    op.execute("DELETE FROM categories")
