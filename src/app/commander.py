from dataclasses import dataclass

from ..app.machine_state import State
from ..client.interface import BaseClient
from ..errors.app_errors import BaseAppError
from ..app.machine_state import StateMachine
from ..services.income_service import MakeIncomeService
from ..services.expense_service import MakeExpenseService
from ..app.machine_commands import CommandsMachine, Commands
from ..services.category_service import CategoryActionsService
from ..config.config import STARTING_MESSAGE, WRONG_INPUT, CANCEL_MESSAGE
from ..app.client_info import UserInformation, UserStateInfo, UserLastInfo


# TODO: UpdatesConsumer
# Должен считывать апдейты из телеграма и преобразовывать апдейд к нашей доменной области,
# к примеру ClientsInfo -> Event, после этого он отдает эти ивенты на обработку другой сущности EventProcessor

# update = {'user_info': 'Ivan Ivanov 993'} -> Event = {'first_name': 'Ivan', 'last_name': 'Ivanov', 'birth_date': 993}
# update = {'full_name': 'Ivan Ivanov', 'date': 993} -> --//--


class Commander:
    """
    Class processes the received messages from the Telegram api and then launches the necessary services
    """

    def __init__(
        self,
        client: BaseClient,
        income_service: MakeIncomeService,
        expense_service: MakeExpenseService,
        category_service: CategoryActionsService,
    ):
        self.client = client
        self.income_service = income_service
        self.expense_service = expense_service
        self.category_service = category_service
        self.last_update_id = 0

    def manage(self, clients: dict[int: ClientStateInfo]):
        updates = self.client.get_update(self.last_update_id)

        if updates:
            for update in updates:
                # TODO: converting client_info
                client_information = ClientInformation(
                    update["message"]["from"]["first_name"],
                    update["update_id"],
                    update["message"]["chat"]["id"],
                    update["message"]["text"].strip().lower(),
                )
                # TODO: если у пользователя запущена statemachine, то мы ждем от него любой ввод, но не команду,
                #  а если машина на нуле, то мы ждем от него только команду и все остальное не валидно
                self.last_update_id = update["update_id"] + 1
                try:
                    if client_information.chat_id not in clients.keys():
                        client_state_info = ClientStateInfo(
                            StateMachine(), CommandsMachine(), ClientLastInfo(client_information.chat_id)
                        )
                        clients[client_information.chat_id] = client_state_info
                    else:
                        client_state_info = clients[client_information.chat_id]

                    if client_information.text in ("/start", "/help"):
                        client_state_info.state.change_state(State.START)
                        client_state_info.command.change_command(Commands.NONE)
                        client_state_info.last_info = ClientLastInfo(
                            client_information.chat_id
                        )
                        self.client.send_message(
                            client_information.chat_id, STARTING_MESSAGE
                        )
                    elif client_information.text == "/cancel":
                        client_state_info.state.change_state(State.START)
                        client_state_info.command.change_command(Commands.NONE)
                        client_state_info.last_info = ClientLastInfo(
                            client_information.chat_id
                        )
                        self.client.send_message(
                            client_information.chat_id, CANCEL_MESSAGE
                        )
                    elif (
                        client_information.text == "/make_income" or
                        client_state_info.command.current_command == Commands.MAKE_INCOME
                    ):
                        client_state_info = self.income_service.make_income(
                            client_information, client_state_info
                        )
                        clients[client_information.chat_id] = client_state_info
                    elif (
                        client_information.text == "/make_expense"
                        or client_state_info.command.current_command
                        == Commands.MAKE_EXPENSE
                    ):
                        client_state_info = self.expense_service.make_expense(
                            client_information, client_state_info
                        )
                        clients[client_information.chat_id] = client_state_info
                    elif client_information.text == "/get_income_categories":
                        client_state_info = self.category_service.get_income_categories(
                            client_information, client_state_info
                        )
                        clients[client_information.chat_id] = client_state_info
                    elif client_information.text == "/get_expense_categories":
                        client_state_info = (
                            self.category_service.get_expense_categories(
                                client_information, client_state_info
                            )
                        )
                        clients[client_information.chat_id] = client_state_info
                    elif (
                        client_information.text == "/delete_income_categories"
                        or client_state_info.command.current_command
                        == Commands.DELETE_INCOME_CATEGORIES
                    ):
                        client_state_info = (
                            self.income_service.delete_income_categories(
                                client_information, client_state_info
                            )
                        )
                        clients[client_information.chat_id] = client_state_info
                    elif (
                        client_information.text == "/delete_expense_categories"
                        or client_state_info.command.current_command
                        == Commands.DELETE_EXPENSE_CATEGORIES
                    ):
                        client_state_info = (
                            self.expense_service.delete_expense_categories(
                                client_information, client_state_info
                            )
                        )
                        clients[client_information.chat_id] = client_state_info
                    else:
                        self.client.send_message(client_information.chat_id, WRONG_INPUT)
                except BaseAppError as error:
                    self.client.send_message(client_information.chat_id, error.msg)

        return clients


# def command_resolver(command):
#     action_for_command = {'make_income': make_income}
#     action = action_for_command[command]
#     action()  # action(params)
#
# def state_resolver(state):
#     action_for_state = {'make_income': make_state}
#     action = action_for_state[state]
#     action()  # action(params)

# class StateMachine:
#     def go_next_state(self):
#         pass
#
#     def get_current_state(self):
#         pass
#
# class IncomeStateMachine:
#     _mapping = {'make_income': 'input_amount', 'input_amount': 'save_income'}
#
#     def go_next_state(self):
#         if get_current_state == make_income:
#             self._mapping['make_income']
