from dataclasses import dataclass

from .machine_state import StateMachine
from ..client.interface import BaseClient
from .event_processor import EventProcessor
from ..errors.app_errors import BaseAppError
from .machine_commands import CommandsMachine
from ..state_machine.interface import BaseStateMachine
from ..app.client_info import UserStateInfo, UserLastInfo


@dataclass
class User:
    first_name: str
    update_id: int
    chat_id: int
    text: str


@dataclass
class Event:
    user: User
    command: bool
    state_machine: BaseStateMachine | None


# Все команды, кроме /cancel, т.к. ее нужно проверять отдельно
# для возможности отмены действия в любом состоянии StateMachine
commands = [
    '/make_income', '/make_expense', '/get_income_categories'
    '/get_expense_categories', '/delete_income_categories', '/delete_expense_categories'
]


class UpdatesConsumer:
    """
    Class processes the received messages from the Telegram api and then sent "Event" to EventProcessor
    """
    def __init__(
            self,
            client: BaseClient,
            event_processor: EventProcessor
    ):
        self.client = client
        self.event_processor = event_processor
        self._last_update_id = 0

    def update_consumer(self, users: dict[int: UserStateInfo]):
        updates = self.client.get_update(self._last_update_id)

        if updates:
            for update in updates:
                user = self._converting_update(update)
                try:
                    user_state_info, users = self._get_or_init_user_state_info(user, users)
                    users = self.event_processor.processing(user, user_state_info, users)
                    return users
                except BaseAppError as error:
                    self.client.send_message(user.chat_id, error.msg)

    def _converting_update(self, update: dict) -> User:
        user = User(
            update["message"]["from"]["first_name"],
            update["update_id"],
            update["message"]["chat"]["id"],
            update["message"]["text"].strip().lower()
        )
        self._last_update_id = update["update_id"] + 1
        return user

    @staticmethod
    def _get_or_init_user_state_info(user: User, users: dict[str: UserStateInfo]):
        if user.chat_id not in users.keys():
            user_state_info = UserStateInfo(
                StateMachine(), CommandsMachine(), UserLastInfo(user.chat_id)
            )
            users[user.chat_id] = user_state_info
        else:
            user_state_info = users[user.chat_id]
        return user_state_info, users
