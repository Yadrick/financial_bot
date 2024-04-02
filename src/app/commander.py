from dataclasses import dataclass

from ..app.machine_state import StateMachine
from ..app.machine_commands import CommandsMachine, Commands
from ..client.client import ClientInformation
from ..client.interface import BaseClient
from ..services.income_service import MakeIncomeService
from src.services.expense_service import MakeExpenseService
from ..config.config import STARTING_MESSAGE, WRONG_INPUT


@dataclass
class ClientStateInfo:
    state: StateMachine
    last_info: dict
    command: CommandsMachine


class Commander:
    """
    Class processes the received messages from the Telegram api and then launches the necessary services
    """

    def __init__(
        self,
        client: BaseClient,
        make_income_service: MakeIncomeService,
        make_expense_service: MakeExpenseService,
    ):
        self.client = client
        self.make_income_service = make_income_service
        self.make_expense_service = make_expense_service
        self.last_update_id = 0

    def manage(self, clients: dict[int:ClientStateInfo]):
        updates = self.client.get_update(self.last_update_id)

        if updates:
            for update in updates:
                client_information = ClientInformation(
                    update["message"]["from"]["first_name"],
                    update["update_id"],
                    update["message"]["chat"]["id"],
                    update["message"]["text"],
                )
                self.last_update_id = update["update_id"] + 1

                if client_information.chat_id not in clients.keys():
                    state = StateMachine()
                    command = CommandsMachine()
                    last_info = {}
                    clients[client_information.chat_id] = ClientStateInfo(
                        state, last_info, command
                    )
                else:
                    client_state_info = clients[client_information.chat_id]
                    state = client_state_info.state
                    command = client_state_info.command
                    last_info = client_state_info.last_info

                if client_information.text in ("/start", "/help"):
                    self.client.send_message(
                        client_information.chat_id, STARTING_MESSAGE
                    )
                elif (
                    client_information.text == "/make_income"
                    or clients[client_information.chat_id].command.current_command
                    == Commands.MAKE_INCOME
                ):
                    state, last_info, command = self.make_income_service.make_income(
                        update["message"]["text"],
                        state,
                        last_info,
                        update["message"]["chat"]["id"],
                        command,
                    )
                    clients[client_information.chat_id] = ClientStateInfo(
                        state, last_info, command
                    )
                elif (
                    client_information.text == "/make_expense"
                    or clients[client_information.chat_id].command.current_command
                    == Commands.MAKE_EXPENSE
                ):
                    state, last_info, command = self.make_expense_service.make_expense(
                        update["message"]["text"],
                        state,
                        last_info,
                        update["message"]["chat"]["id"],
                        command,
                    )
                    clients[client_information.chat_id] = ClientStateInfo(
                        state, last_info, command
                    )
                else:
                    self.client.send_message(client_information.chat_id, WRONG_INPUT)
                return clients
