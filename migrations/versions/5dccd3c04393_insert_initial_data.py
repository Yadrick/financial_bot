"""insert_initial_data

Revision ID: 5dccd3c04393
Revises: 344a2bb084ed
Create Date: 2024-04-10 22:20:40.760942

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "5dccd3c04393"
down_revision: Union[str, None] = "344a2bb084ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO categories (name, type)
        VALUES
            ('Зарплата', 'income'),
            ('Продукты', 'expense'),
            ('Премия', 'income'),
            ('Кафе', 'expense'),
            ('Налоги', 'expense')
        """
    )


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("categories")
    op.drop_table("transactions")
