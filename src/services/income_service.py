from ..app.machine_state import StateMachine, State
from ..client.interface import BaseClient
from ..repository.interface import BaseRepository
from ..config.config import (
    MESSAGE_ENTER_DATE,
    MESSAGE_ENTER_CATEGORY,
    MESSAGE_ENTER_AMOUNT,
    MESSAGE_SUCCESS
)


class MakeIncomeService:
    """
    Service for making income
    """
    def __init__(self, client: BaseClient, repository: BaseRepository):
        self.client = client
        self.repository = repository

    def make_income(self, text: str, state: StateMachine, last_info: dict, chat_id: int) -> tuple[StateMachine, dict]:
        if state.current_state == State.START:
            self.client.send_message(chat_id, MESSAGE_ENTER_CATEGORY)
            state.change_state(State.RECEIVED_CATEGORY)
            return state, last_info
        elif state.current_state == State.RECEIVED_CATEGORY:
            last_info['category'] = text
            self.client.send_message(chat_id, MESSAGE_ENTER_DATE)
            state.change_state(State.RECEIVED_DATE)
            return state, last_info
        elif state.current_state == State.RECEIVED_DATE:
            last_info['date'] = text
            self.client.send_message(chat_id, MESSAGE_ENTER_AMOUNT)
            state.change_state(State.RECEIVED_AMOUNT)
            return state, last_info
        elif state.current_state == State.RECEIVED_AMOUNT:
            last_info['amount'] = text
            self.client.send_message(chat_id, MESSAGE_SUCCESS)
            self.repository.save(last_info)
            state.change_state(State.START)
            last_info = {}
            return state, last_info
