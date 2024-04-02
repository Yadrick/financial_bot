import os
from dotenv import load_dotenv

load_dotenv()

API_token = os.getenv("API_token")
API_Link = "https://api.telegram.org/bot{API_token}/"


STARTING_MESSAGE = """Привет! Я бот, который поможет тебе вести учет своих доходов и расходов.
Что я умею?
- запоминать доходы по твоим кастомным категориям. Чтобы начать, введи /make_income
- запоминать расходы по твоим кастомным категориям. Чтобы начать, введи /make_expense
- пока только это
- Можете ввести /help или /start для повторного просмотра этого сообщения.
"""

MESSAGE_ENTER_CATEGORY = """Введите или выберите категорию:
- а ничего нет и пока не будет, введите категорию
"""

MESSAGE_ENTER_DATE_INCOME = """Введите дату, за которую хотите внести доходы
(формат dd-mm-yyyy)
P.S. пока можно в любом формате
"""

MESSAGE_ENTER_DATE_EXPENSE = """Введите дату, за которую хотите внести расходы
(формат dd-mm-yyyy)
P.S. пока можно в любом формате
"""

MESSAGE_ENTER_AMOUNT = """Введите сумму (формат 12345.12)"""

MESSAGE_SUCCESS_INCOME = """Запись успешно создана и сохранена"""
MESSAGE_SUCCESS_EXPENSE = """Запись успешно создана и сохранена"""

WRONG_INPUT = """Введите одну из доступных команд"""
