from src.app.app import TelegramBotApp
from src.app.commander import Commander
from src.config.config import API_token
from src.client.client import TelegramClient
from src.services.income_service import MakeIncomeService
from src.services.expense_service import MakeExpenseService
from src.repository.repository import PostgreSQLRepository


def main():
    client = TelegramClient(API_token)
    repository = PostgreSQLRepository()
    make_income_service = MakeIncomeService(client, repository)
    make_expense_service = MakeExpenseService(client, repository)
    commander = Commander(client, make_income_service, make_expense_service)

    app = TelegramBotApp(commander)
    app.start()


if __name__ == "__main__":
    main()
