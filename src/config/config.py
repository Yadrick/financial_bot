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

MESSAGE_ENTER_CATEGORY = """Введите или выберите категорию:\n"""

MESSAGE_ENTER_DATE = (
    """Введите дату, за которую хотите внести доходы \n(формат dd-mm-yyyy)"""
)

MESSAGE_ENTER_AMOUNT = """Введите сумму \n(формат 12345.12)"""

WRONG_INPUT = """Введите одну из доступных команд"""

WRONG_INPUT_DATE = (
    """Некорректный формат даты, попробуйте ещё раз \n(формат dd-mm-yyyy)"""
)

WRONG_INPUT_AMOUNT = (
    """Некорректный формат суммы, попробуйте ещё раз \n(формат 12345.12)"""
)

SAVED_RECORD = """Запись успешно создана и сохранена
\nСохраненная запись:
Категория -> {category}
Дата -> {date}
Сумма -> {amount}
"""
