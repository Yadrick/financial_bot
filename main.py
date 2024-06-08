from src.app.app import TelegramBotApp
from src.app.commander import Commander
from src.config.config import API_token
from src.client.client import TelegramClient
from src.services.income_service import MakeIncomeService
from src.services.expense_service import MakeExpenseService
from src.services.category_service import CategoryActionsService
from src.repository.repository import PostgreSQLRepository
from src.services.personal_report_service import ReportService

import psycopg
import os
from dotenv import load_dotenv

load_dotenv(".env.local")

pg_host = os.getenv("PG_HOST")
pg_port = os.getenv("PG_PORT")
pg_user = os.getenv("POSTGRES_USER")
pg_password = os.getenv("POSTGRES_PASSWORD")
pg_db = os.getenv("POSTGRES_DB")

conn_string = f"host={pg_host} port={pg_port} dbname={pg_db} user={pg_user} password={pg_password}"


def main():
    try:
        conn = psycopg.connect(conn_string)
        client = TelegramClient(API_token)
        repository = PostgreSQLRepository(conn)
        make_income_service = MakeIncomeService(client, repository)
        make_expense_service = MakeExpenseService(client, repository)
        category_service = CategoryActionsService(client, repository)
        personal_report_service = ReportService(client, repository)
        commander = Commander(
            client,
            make_income_service,
            make_expense_service,
            category_service,
            personal_report_service,
        )

        app = TelegramBotApp(commander)
        app.start()
    except Exception as ex:
        print(f"Error in main: {ex}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
