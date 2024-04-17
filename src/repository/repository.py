from .categories import Categories
from ..app.client_info import ClientLastInfo
from ..repository.interface import BaseRepository
import psycopg2


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
            self.connect.commit()
            cursor.close()
        except psycopg2.Error as e:
            print("Error:", e)

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
            self.connect.commit()
            cursor.close()
        except psycopg2.Error as e:
            print("Error:", e)

    def save_transaction(self, last_info: ClientLastInfo):
        try:
            cursor = self.connect.cursor()
            query_trans = "INSERT INTO transactions (date, amount_money, category_name, user_id) VALUES ( %s, %s, %s, %s);"
            cursor.execute(
                query_trans,
                (
                    last_info.date,
                    last_info.amount,
                    last_info.category,
                    last_info.chat_id,
                ),
            )
            self.connect.commit()
            cursor.close()

        except psycopg2.Error as e:
            print("Error:", e)

    def get_categories(self, type_category: str, chat_id: str) -> Categories:
        """
        type_category: income or expense
        """
        try:
            cursor = self.connect.cursor()
            cursor.execute(
                f"SELECT name FROM categories WHERE type = '{type_category}' AND (user_id IS NULL OR user_id = {chat_id}) "
            )

            categories = [row[0] for row in cursor.fetchall()]

            cursor.close()

            return Categories(categories)

        except psycopg2.Error as e:
            print("Error:", e)
            return None
