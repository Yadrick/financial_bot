import psycopg

from .categories import Categories
from ..app.event import Event
from ..repository.interface import BaseRepository
from .interface_for_transactions_to_save import BaseTransactionInfo


class PostgreSQLRepository(BaseRepository):
    """
    Class for communication with PostgreSQL
    """

    def __init__(self, connection):
        self.connect = connection

    def save(self, transaction_info: BaseTransactionInfo):
        try:
            cursor = self.connect.cursor()
            query_users = """
                INSERT INTO users (id, name) SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM users WHERE id = %s);
            """
            query_category = """
                INSERT INTO categories (name, type, user_id) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name = %s);
            """
            query_id_category = """
                SELECT id FROM categories WHERE name = %s AND user_id = %s AND type = %s
            """
            query_trans = """
                INSERT INTO transactions (date, amount_money, category_id, user_id) VALUES ( %s, %s, %s, %s);
            """

            cursor.execute(
                query_users,
                (
                    transaction_info.chat_id,
                    transaction_info.first_name,
                    transaction_info.chat_id,
                ),
            )
            cursor.execute(
                query_category,
                (
                    transaction_info.category,
                    transaction_info.type_category,
                    transaction_info.chat_id,
                    transaction_info.category,
                ),
            )

            cursor.execute(
                query_id_category,
                (transaction_info.category, transaction_info.chat_id, transaction_info.type_category),
            )
            category_id = cursor.fetchone()

            cursor.execute(
                query_trans,
                (
                    transaction_info.date,
                    transaction_info.amount,
                    category_id[0],
                    transaction_info.chat_id,
                ),
            )

        except psycopg.Error as e:
            print("Error:", e)
        finally:
            self.connect.commit()
            cursor.close()

    def save_user(self, event: Event):
        try:
            cursor = self.connect.cursor()
            query_users = """
                INSERT INTO users (id, name) SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM users WHERE id = %s);
            """
            cursor.execute(
                query_users,
                (
                    event.user.chat_id,
                    event.user.first_name,
                    event.user.chat_id,
                ),
            )
        except psycopg.Error as e:
            print("Error:", e)
        finally:
            self.connect.commit()
            cursor.close()

    def get_categories(self, type_category: str, chat_id: str) -> Categories:
        """
        type_category: income or expense
        """

        try:
            cursor = self.connect.cursor()
            cursor.execute(
                f"""SELECT name FROM categories WHERE type = '{type_category}' AND user_id = {chat_id} """
            )

            categories = [row[0] for row in cursor.fetchall()]

            return Categories(categories)

        except psycopg.Error as e:
            print("Error:", e)
        finally:
            cursor.close()

    def delete_category_and_related_transactions(
        self, event: Event, type_category: str
    ):
        """
        пу-пу-пу
        """

        try:
            cursor = self.connect.cursor()
            query = "SELECT id FROM categories WHERE name = %s AND user_id = %s AND type = %s"
            query_delete_transactions = (
                "DELETE FROM transactions WHERE category_id = %s AND user_id = %s"
            )
            query_delete_category = "DELETE FROM categories WHERE id = %s"
            cursor.execute(
                query,
                (event.text, event.user.chat_id, type_category),
            )
            category_id = cursor.fetchone()
            if category_id:
                cursor.execute(
                    query_delete_transactions,
                    (
                        category_id[0],
                        event.user.chat_id,
                    ),
                )
                cursor.execute(
                    query_delete_category,
                    category_id,
                )
            return category_id

        except psycopg.Error as e:
            print("Error:", e)
        finally:
            self.connect.commit()
            cursor.close()
