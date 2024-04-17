from ..app.machine_state import StateMachine
from ..app.client_info import ClientStateInfo, ClientLastInfo
from ..app.machine_commands import CommandsMachine, Commands
from ..client.client import ClientInformation
from ..client.interface import BaseClient
from ..errors.app_errors import BaseAppError
from ..services.income_service import MakeIncomeService
from ..services.category_service import CategoryActionsService
from src.services.expense_service import MakeExpenseService
from ..config.config import STARTING_MESSAGE, WRONG_INPUT


class Commander:
    """
    Class processes the received messages from the Telegram api and then launches the necessary services
    """

    def __init__(
        self,
        client: BaseClient,
        make_income_service: MakeIncomeService,
        make_expense_service: MakeExpenseService,
        category_service: CategoryActionsService,
    ):
        self.client = client
        self.make_income_service = make_income_service
        self.make_expense_service = make_expense_service
        self.category_service = category_service
        self.last_update_id = 0

    def manage(self, clients: dict[int:ClientStateInfo]):

        updates = self.client.get_update(self.last_update_id)

        if updates:
            for update in updates:
                client_information = ClientInformation(
                    update["message"]["from"]["first_name"],
                    update["update_id"],
                    update["message"]["chat"]["id"],
                    update["message"]["text"].strip().lower(),
                )
                self.last_update_id = update["update_id"] + 1
                try:
                    if client_information.chat_id not in clients.keys():
                        client_state_info = ClientStateInfo(
                            StateMachine(),
                            CommandsMachine(),
                            ClientLastInfo(client_information.chat_id),
                        )
                        clients[client_information.chat_id] = client_state_info
                    else:
                        client_state_info = clients[client_information.chat_id]

                    if client_information.text in ("/start", "/help"):
                        self.client.send_message(
                            client_information.chat_id, STARTING_MESSAGE
                        )
                    elif (
                        client_information.text == "/make_income"
                        or clients[client_information.chat_id].command.current_command
                        == Commands.MAKE_INCOME
                    ):
                        client_state_info = self.make_income_service.make_income(
                            client_information, client_state_info
                        )
                        clients[client_information.chat_id] = client_state_info
                    elif (
                        client_information.text == "/make_expense"
                        or clients[client_information.chat_id].command.current_command
                        == Commands.MAKE_EXPENSE
                    ):
                        client_state_info = self.make_expense_service.make_expense(
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
                    else:
                        self.client.send_message(
                            client_information.chat_id, WRONG_INPUT
                        )
                except BaseAppError as error:
                    self.client.send_message(client_information.chat_id, error.msg)

        return clients
