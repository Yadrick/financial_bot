from dataclasses import dataclass

from ..app.machine_state import StateMachine, State
from ..client.client import ClientInformation
from ..client.interface import BaseClient
from ..services.income_service import MakeIncomeService
from ..config.config import STARTING_MESSAGE, WRONG_INPUT


@dataclass
class ClientStateInfo:
    state: StateMachine
    last_info: dict


class Commander:
    """
    Class processes the received messages from the Telegram api and then launches the necessary services
    """
    def __init__(self, client: BaseClient, make_income_service: MakeIncomeService):
        self.client = client
        self.make_income_service = make_income_service
        self.last_update_id = 0

    def manage(self, clients: dict[int: ClientStateInfo]):
        updates = self.client.get_update(self.last_update_id)

        if updates:
            for update in updates:
                client_information = ClientInformation(  # TODO: Check fields in 'update'
                    update['message']['from']['first_name'],
                    update['update_id'],
                    update['message']['chat']['id'],
                    update['message']['text'],
                )
                self.last_update_id = update['update_id'] + 1

                if client_information.chat_id not in clients.keys():
                    state = StateMachine()
                    last_info = {}
                    clients[client_information.chat_id] = ClientStateInfo(state, last_info)
                else:
                    client_state_info = clients[client_information.chat_id]
                    state = client_state_info.state
                    last_info = client_state_info.last_info

                if client_information.text in ('/start', '/help'):
                    self.client.send_message(client_information.chat_id, STARTING_MESSAGE)
                elif client_information.text == '/make_income' or (
                        clients[client_information.chat_id].state.current_state != State.START
                ):
                    state, last_info = self.make_income_service.make_income(
                        update['message']['text'],
                        state,
                        last_info,
                        update['message']['chat']['id']
                    )
                    clients[update['message']['chat']['id']] = ClientStateInfo(state, last_info)
                else:
                    self.client.send_message(client_information.chat_id, WRONG_INPUT)
                return clients
