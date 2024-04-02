from ..app.machine_state import StateMachine, State
from ..app.machine_commands import CommandsMachine, Commands
from ..client.interface import BaseClient
from ..repository.interface import BaseRepository
from ..config.config import (
    MESSAGE_ENTER_DATE_INCOME,
    MESSAGE_ENTER_CATEGORY,
    MESSAGE_ENTER_AMOUNT,
    MESSAGE_SUCCESS_INCOME,
)


class MakeIncomeService:
    """
    Service for making income
    """

    def __init__(self, client: BaseClient, repository: BaseRepository):
        self.client = client
        self.repository = repository

    def make_income(
        self,
        text: str,
        state: StateMachine,
        last_info: dict,
        chat_id: int,
        command: CommandsMachine,
    ) -> tuple[StateMachine, dict]:
        if state.current_state == State.START:
            self.client.send_message(chat_id, MESSAGE_ENTER_CATEGORY)
            state.change_state(State.RECEIVED_CATEGORY)
            command.change_command(Commands.MAKE_INCOME)
            return state, last_info, command
        elif state.current_state == State.RECEIVED_CATEGORY:
            last_info["category"] = text
            self.client.send_message(chat_id, MESSAGE_ENTER_DATE_INCOME)
            state.change_state(State.RECEIVED_DATE)
            return state, last_info, command
        elif state.current_state == State.RECEIVED_DATE:
            last_info["date"] = text
            self.client.send_message(chat_id, MESSAGE_ENTER_AMOUNT)
            state.change_state(State.RECEIVED_AMOUNT)
            return state, last_info, command
        elif state.current_state == State.RECEIVED_AMOUNT:
            last_info["amount"] = text
            self.client.send_message(chat_id, MESSAGE_SUCCESS_INCOME)
            self.repository.save(last_info)
            state.change_state(State.START)
            command.change_command(Commands.NONE)
            last_info = {}
            return state, last_info, command
