import os
import traceback

import psycopg

from dotenv import load_dotenv

from src.app.app import TelegramBotApp
from src.config.config import API_token
from src.client.client import TelegramClient
from src.app.event_processor import EventProcessor
from src.app.update_consumer import UpdatesConsumer
from src.repository.repository import PostgreSQLRepository
from src.services.category_service import CategoryActionsService


load_dotenv(".env.local")

pg_host = os.getenv("PG_HOST")
pg_port = os.getenv("PG_PORT")
pg_user = os.getenv("POSTGRES_USER")
pg_password = os.getenv("POSTGRES_PASSWORD")
pg_db = os.getenv("POSTGRES_DB")

conn_string = f"host={pg_host} port={pg_port} dbname={pg_db} user={pg_user} password={pg_password}"


def main():
    conn = psycopg.connect(conn_string)
    try:
        client = TelegramClient(API_token)
        repository = PostgreSQLRepository(conn)

        category_service = CategoryActionsService(client, repository)

        event_processor = EventProcessor(
            client, category_service
        )
        updates_consumer = UpdatesConsumer(
            client, event_processor, repository,
        )
        app = TelegramBotApp(updates_consumer)

        app.start()
    except Exception as error:
        print(f"Error in main: {error}\n{traceback.format_exc()}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
