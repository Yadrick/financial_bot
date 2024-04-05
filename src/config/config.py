import os
from dotenv import load_dotenv

load_dotenv()

API_token = os.getenv("API_token")
API_Link = "https://api.telegram.org/bot{API_token}/"


STARTING_MESSAGE = """Привет! Я бот, который поможет тебе вести учет своих доходов и расходов.
Что я умею?
- Запоминать доходы по твоим кастомным категориям. Чтобы начать, введи /make_income
- Можете ввести /help или /start для повторного просмотра этого сообщения.
"""

MESSAGE_ENTER_CATEGORY = """Введите или выберите категорию:"""

MESSAGE_ENTER_DATE = """Введите дату, за которую хотите внести доходы (формат dd-mm-yyyy)"""

MESSAGE_ENTER_AMOUNT = """Введите сумму (формат 12345.12)"""

MESSAGE_SUCCESS = """Запись успешно создана и сохранена"""

WRONG_INPUT = """Введите одну из доступных команд"""

WRONG_INPUT_CATEGORY = """Данной категории нет в вашем списке категорий,
                          введите уже существующую или сначала сохраните её"""

WRONG_INPUT_DATE = """Некорректный формат даты, попробуйте ещё раз (формат dd-mm-yyyy)"""

WRONG_INPUT_AMOUNT = """Некорректный формат суммы, попробуйте ещё раз (формат 12345.12)"""
