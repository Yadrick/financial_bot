import psycopg

from .categories import Categories
from ..app.client_info import ClientLastInfo
from ..repository.interface import BaseRepository


class PostgreSQLRepository(BaseRepository):
    """
    Class for communication with PostgreSQL
    """

    def __init__(self, connection):
        self.connect = connection

    def save_user(self, last_info: ClientLastInfo):
        try:
            cursor = self.connect.cursor()
            query_users = """
INSERT INTO users (id, name) SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM users WHERE id = %s);
"""
            cursor.execute(
                query_users,
                (
                    last_info.chat_id,
                    last_info.name,
                    last_info.chat_id,
                ),
            )
        except psycopg.Error as e:
            print("Error:", e)
        finally:
            self.connect.commit()
            cursor.close()

    def save_category(self, last_info: ClientLastInfo, type_category: str):
        try:
            cursor = self.connect.cursor()
            query_category = """
INSERT INTO categories (name, type, user_id) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name = %s);
"""
            cursor.execute(
                query_category,
                (
                    last_info.category,
                    type_category,
                    last_info.chat_id,
                    last_info.category,
                ),
            )
        except psycopg.Error as e:
            print("Error:", e)
        finally:
            self.connect.commit()
            cursor.close()

    def save_transaction(self, last_info: ClientLastInfo, type_category: str):
        try:
            cursor = self.connect.cursor()
            query_id_category = "SELECT id FROM categories WHERE name = %s AND user_id = %s AND type = %s"
            cursor.execute(
                query_id_category,
                (last_info.category, last_info.chat_id, type_category),
            )
            category_id = cursor.fetchone()
            query_trans = "INSERT INTO transactions (date, amount_money, category_id, user_id) VALUES ( %s, %s, %s, %s);"
            cursor.execute(
                query_trans,
                (
                    last_info.date,
                    last_info.amount,
                    category_id[0],
                    last_info.chat_id,
                ),
            )
        except psycopg.Error as e:
            print("Error:", e)
        finally:
            self.connect.commit()
            cursor.close()

    def get_categories(self, type_category: str, chat_id: int) -> Categories:
        """
        type_category: income or expense
        """
        try:
            cursor = self.connect.cursor()
            cursor.execute(
                f"SELECT name FROM categories WHERE type = '{type_category}' AND user_id = {chat_id} "
            )

            categories = [row[0] for row in cursor.fetchall()]

            return Categories(categories)

        except psycopg.Error as e:
            print("Error:", e)
            return None
        finally:
            cursor.close()

    def delete_category_and_related_transactions(
        self, last_info: ClientLastInfo, type_category: str
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
                (last_info.category, last_info.chat_id, type_category),
            )
            category_id = cursor.fetchone()
            if category_id:
                cursor.execute(
                    query_delete_transactions,
                    (
                        category_id[0],
                        last_info.chat_id,
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
