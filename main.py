import requests


from enum import Enum, auto

from src.config.config import (
    API_Link,
    API_token,
    STARTING_MESSAGE,
    MESSAGE_AFTER_MAKE_INCOME,
    MESSAGE_ENTER_DATE,
    MESSAGE_ENTER_SUM,
)


class State(Enum):
    START = auto()
    MAKE_INCOME = auto()
    MAKE_EXPENSE = auto()
    GET_INCOME_CATEGORIES = auto()
    GET_EXPENSE_CATEGORIES = auto()
    DELETE_INCOME_CATEGORIES = auto()
    DELETE_EXPENSE_CATEGORIES = auto()
    REPORT_PER_DAY = auto()
    REPORT_PER_MONTH = auto()
    REPORT_PER_PERIOD = auto()


class StateMakeIncome(Enum):
    # базовое состояние - Make_Income. Далее просят ввестикатегорию
    START = auto()
    GET_CATEGORY = auto()  # соостояние до и после успешно введенной категории
    GET_DATE = auto()  # состояние после успешно введенной даты
    GET_AMOUNT = auto()  # состояние после успешно введенной суммы
    # дальше выводится сводкка по введенным пользователем данным. Он может оставить как есть или удалить
    READY = auto()  # хз нужно ли, можно просто состояние перевести на START


def send_message(chat_id, text):
    url = API_Link.format(API_token=API_token) + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=data)
    return response.json()


def function1(chat_id, text, state):
    if text == "/make_income":
        send_message(
            chat_id,
            MESSAGE_AFTER_MAKE_INCOME,
        )
        return StateMakeIncome.GET_CATEGORY
    elif state == StateMakeIncome.GET_CATEGORY:
        send_message(chat_id, MESSAGE_ENTER_DATE)
        return StateMakeIncome.GET_DATE
    elif state == StateMakeIncome.GET_DATE:
        send_message(chat_id, MESSAGE_ENTER_SUM)
        return StateMakeIncome.GET_AMOUNT
    elif state == StateMakeIncome.GET_AMOUNT:
        send_message(
            chat_id,
            "Итого: бла-бла. Все классно, "
            + "теперь можете продолжать вводить команды. Для их просмотра введите /help",
        )
        return State.START
    else:
        send_message(chat_id, "Неизвестно:")

    return State.START


# можно в каждом if запускать свой метод по работе со своим состоянием, в котором будет прописана логика продолжения
def handle_message(chat_id, text, state):
    if text == "/start" or text == "/help":
        send_message(chat_id, STARTING_MESSAGE)
        return State.START
    elif text == "/make_income" or state in StateMakeIncome:
        return function1(chat_id, text, state)
    # elif text == "/make_expense":
    #     send_message(chat_id, "Введите категорию для расхода:")
    #     return State.MAKE_EXPENSE
    # elif text == "/get_income_categories":
    #     # Реализация получения категорий для доходов
    #     return State.GET_INCOME_CATEGORIES
    # elif text == "/get_expense_categories":
    #     # Реализация получения категорий для расходов
    #     return State.GET_EXPENSE_CATEGORIES
    # elif text == "/delete_income_categories":
    #     # Реализация удаления категорий для доходов
    #     return State.DELETE_INCOME_CATEGORIES
    # elif text == "/delete_expense_categories":
    #     # Реализация удаления категорий для расходов
    #     return State.DELETE_EXPENSE_CATEGORIES
    # elif text == "/report_per_day":
    #     # Реализация отчетов по дням
    #     return State.REPORT_PER_DAY
    # elif text == "/report_per_month":
    #     # Реализация отчетов по месяцам
    #     return State.REPORT_PER_MONTH
    # elif text == "/report_per_period":
    #     # Реализация отчетов за период
    #     return State.REPORT_PER_PERIOD
    else:
        send_message(
            chat_id,
            "Неизвестная команда. Пожалуйста, используйте одну из предложенных команд."
            + "Введите /start или /help для просмотра.",
        )
        return State.START

    # Другие состояния обработки команд
    # ...

    # for update in updates["result"]:
    #     chat_id = update["message"]["chat"]["id"]
    #     if "text" in update["message"]:
    #         text = update["message"]["text"]
    #         current_state = handle_message(chat_id, text, current_state)


def main():
    user_and_state = {}
    last_update_id = 0
    while True:

        updates = requests.get(
            API_Link.format(API_token=API_token) + "getUpdates",
            params={
                "offset": last_update_id,
                "timeout": 30,
            },
        ).json()

        if "result" in updates:
            # Обрабатываем каждое новое обновление
            for update in updates["result"]:
                chat_id = update["message"]["chat"]["id"]
                user_and_state.setdefault(chat_id, State.START)
                text = update["message"]["text"]
                current_state = handle_message(chat_id, text, user_and_state[chat_id])
                user_and_state[chat_id] = current_state

                last_update_id = update["update_id"] + 1
                print(user_and_state)


if __name__ == "__main__":
    main()
