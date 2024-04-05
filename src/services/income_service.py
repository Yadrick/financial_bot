from datetime import datetime

from ..app.machine_state import StateMachine, State
from ..app.machine_commands import CommandsMachine, Commands
from ..client.interface import BaseClient
from ..errors.app_errors import WrongInputError
from ..repository.interface import BaseRepository
from ..config.config import (
    MESSAGE_ENTER_DATE,
    MESSAGE_ENTER_CATEGORY,
    MESSAGE_ENTER_AMOUNT,
    MESSAGE_SUCCESS,
    WRONG_INPUT_CATEGORY,
    WRONG_INPUT_DATE,
    WRONG_INPUT_AMOUNT,
)


class MakeIncomeService:
    """
    Service for making income
    """

    def __init__(self, client: BaseClient, repository: BaseRepository):
        self.client = client
        self.repository = repository

    def _start_processing(
            self,
            state: StateMachine,
            last_info: dict,
            chat_id: int,
            command: CommandsMachine,
    ) -> tuple[StateMachine, dict, CommandsMachine]:
        categories = self.repository.get_categories()
        self.client.send_message(chat_id, MESSAGE_ENTER_CATEGORY)
        self.client.send_message(chat_id, str(categories))
        state.change_state(State.RECEIVED_CATEGORY)
        command.change_command(Commands.MAKE_INCOME)
        return state, last_info, command

    def _category_processing(
            self,
            category: str,
            state: StateMachine,
            last_info: dict,
            chat_id: int,
            command: CommandsMachine,
    ) -> tuple[StateMachine, dict, CommandsMachine]:

        categories = self.repository.get_categories()
        if category not in categories:
            raise WrongInputError(WRONG_INPUT_CATEGORY)
        else:
            last_info['category'] = category
            self.client.send_message(chat_id, MESSAGE_ENTER_DATE)
            state.change_state(State.RECEIVED_DATE)
            return state, last_info, command

    def _date_processing(
            self,
            input_date: str,
            state: StateMachine,
            last_info: dict,
            chat_id: int,
            command: CommandsMachine,
    ) -> tuple[StateMachine, dict, CommandsMachine]:
        try:
            date = datetime.strptime(input_date, '%d-%m-%Y')
            last_info['date'] = date
            self.client.send_message(chat_id, MESSAGE_ENTER_AMOUNT)
            state.change_state(State.RECEIVED_AMOUNT)
            return state, last_info, command
        except ValueError:
            raise WrongInputError(WRONG_INPUT_DATE)

    def _amount_processing(
            self,
            input_amount: str,
            state: StateMachine,
            last_info: dict,
            chat_id: int,
            command: CommandsMachine,
    ) -> tuple[StateMachine, dict, CommandsMachine]:
        try:
            amount = float(input_amount)
            last_info['amount'] = amount
            self.client.send_message(chat_id, MESSAGE_SUCCESS)
            self.repository.save(last_info)
            state.change_state(State.START)
            command.change_command(Commands.NONE)
            last_info = {}
            return state, last_info, command
        except ValueError:
            raise WrongInputError(WRONG_INPUT_AMOUNT)

    def make_income(
            self,
            text: str,
            state: StateMachine,
            last_info: dict,
            chat_id: int,
            command: CommandsMachine,
    ) -> tuple[StateMachine, dict, CommandsMachine]:
        text = text.lower().strip()
        if state.current_state == State.START:
            output = self._start_processing(state, last_info, chat_id, command)
            return output
        elif state.current_state == State.RECEIVED_CATEGORY:
            output = self._category_processing(text, state, last_info, chat_id, command)
            return output
        elif state.current_state == State.RECEIVED_DATE:
            output = self._date_processing(text, state, last_info, chat_id, command)
            return output
        elif state.current_state == State.RECEIVED_AMOUNT:
            output = self._amount_processing(text, state, last_info, chat_id, command)
            return output
