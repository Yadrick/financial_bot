from datetime import datetime

from ..app.client_info import ClientStateInfo, ClientInformation
from ..app.machine_state import State
from ..app.machine_commands import Commands
from ..client.interface import BaseClient
from ..errors.app_errors import WrongInputError
from ..repository.interface import BaseRepository
from ..config.config import (
    MESSAGE_ENTER_DATE,
    MESSAGE_ENTER_CATEGORY,
    MESSAGE_ENTER_AMOUNT,
    WRONG_INPUT_DATE,
    WRONG_INPUT_AMOUNT,
    SAVED_RECORD,
    DELETE_INCOME_CATEGORY_MESSAGE,
    CATEGORY_SUCCESSFULLY_DELETED,
    CATEGORY_NOT_DELETED,
    CATEGORIES_NOT_FOUND,
)


class MakeIncomeService:
    """
    Service for making income
    """

    def __init__(self, client: BaseClient, repository: BaseRepository):
        self.client = client
        self.repository = repository
        self.type_category = "income"

    def _start_processing(
        self, client_information: ClientInformation, client_state_info: ClientStateInfo
    ) -> ClientStateInfo:
        client_state_info.state.change_state(State.RECEIVED_CATEGORY)
        client_state_info.command.change_command(Commands.MAKE_INCOME)
        client_state_info.last_info.chat_id = client_information.chat_id
        client_state_info.last_info.name = client_information.first_name
        categories = self.repository.get_categories(
            self.type_category, client_state_info.last_info.chat_id
        )
        self.client.send_message(
            client_information.chat_id, MESSAGE_ENTER_CATEGORY + str(categories)
        )
        self.repository.save_user(client_state_info.last_info)
        return client_state_info

    def _category_processing(
        self, client_information: ClientInformation, client_state_info: ClientStateInfo
    ) -> ClientStateInfo:
        category = client_information.text.capitalize()
        client_state_info.last_info.category = category
        client_state_info.state.change_state(State.RECEIVED_DATE)
        self.client.send_message(client_information.chat_id, MESSAGE_ENTER_DATE)
        return client_state_info

    def _date_processing(
        self, client_information: ClientInformation, client_state_info: ClientStateInfo
    ) -> ClientStateInfo:
        try:
            date = datetime.strptime(client_information.text, "%d-%m-%Y")
            client_state_info.last_info.date = date
            client_state_info.state.change_state(State.RECEIVED_AMOUNT)
            self.client.send_message(client_information.chat_id, MESSAGE_ENTER_AMOUNT)
            return client_state_info
        except ValueError:
            raise WrongInputError(WRONG_INPUT_DATE)

    def _amount_processing(
        self, client_information: ClientInformation, client_state_info: ClientStateInfo
    ) -> ClientStateInfo:
        try:
            amount = float(client_information.text)
            client_state_info.last_info.amount = amount
            client_state_info.state.change_state(State.START)
            client_state_info.command.change_command(Commands.NONE)
            self.repository.save(client_state_info.last_info, self.type_category)
            message = SAVED_RECORD.format(
                category=client_state_info.last_info.category,
                date=client_state_info.last_info.date.strftime("%d-%m-%Y"),
                amount=client_state_info.last_info.amount,
            )
            self.client.send_message(client_information.chat_id, message)

            return client_state_info
        except ValueError:
            raise WrongInputError(WRONG_INPUT_AMOUNT)

    def make_income(
        self, client_information: ClientInformation, client_state_info: ClientStateInfo
    ) -> ClientStateInfo:
        state = client_state_info.state
        if state.current_state == State.START:
            output = self._start_processing(client_information, client_state_info)
            return output
        elif state.current_state == State.RECEIVED_CATEGORY:
            output = self._category_processing(client_information, client_state_info)
            return output
        elif state.current_state == State.RECEIVED_DATE:
            output = self._date_processing(client_information, client_state_info)
            return output
        elif state.current_state == State.RECEIVED_AMOUNT:
            output = self._amount_processing(client_information, client_state_info)
            return output

    def delete_income_categories(
        self, client_information: ClientInformation, client_state_info: ClientStateInfo
    ):
        state = client_state_info.state
        if state.current_state == State.START:
            client_state_info.last_info.chat_id = client_information.chat_id
            categories = self.repository.get_categories(
                "income", client_state_info.last_info.chat_id
            )
            if categories:
                client_state_info.state.change_state(State.WHAITING_CATEGORY)
                client_state_info.command.change_command(
                    Commands.DELETE_INCOME_CATEGORIES
                )
                self.client.send_message(
                    client_information.chat_id,
                    DELETE_INCOME_CATEGORY_MESSAGE + str(categories),
                )
            else:
                self.client.send_message(
                    client_information.chat_id,
                    CATEGORIES_NOT_FOUND,
                )
            return client_state_info
        elif state.current_state == State.WHAITING_CATEGORY:
            category = client_information.text.capitalize()
            client_state_info.last_info.category = category
            result = self.repository.delete_category_and_related_transactions(
                client_state_info.last_info, self.type_category
            )
            if result:
                client_state_info.state.change_state(State.START)
                client_state_info.command.change_command(Commands.NONE)
                self.client.send_message(
                    client_information.chat_id, CATEGORY_SUCCESSFULLY_DELETED
                )
            else:
                self.client.send_message(
                    client_information.chat_id, CATEGORY_NOT_DELETED
                )
            return client_state_info
