from .event import Event, User
from ..client.interface import BaseClient
from .event_processor import EventProcessor
from ..errors.app_errors import BaseAppError
from ..repository.interface import BaseRepository
from ..state_machine.interface import BaseStateMachine
from ..state_machine.income_state_machine import IncomeStateMachine
from ..state_machine.expense_state_machine import ExpenseStateMachine
from ..config.config import WRONG_INPUT, HELP_MESSAGE, CANCEL_MESSAGE
from ..services.income_category_service import IncomeCategoryActionsService
from ..services.expense_category_service import ExpenseCategoryActionsService
from ..state_machine.delete_income_category_state_machine import DeleteIncomeCategoryStateMachine
from ..state_machine.delete_expense_category_state_machine import DeleteExpenseCategoryStateMachine


commands_with_state = {
    '/make_income': IncomeStateMachine,
    '/make_expense': ExpenseStateMachine,
    '/delete_income_categories': DeleteIncomeCategoryStateMachine,
    '/delete_expense_categories': DeleteExpenseCategoryStateMachine,
}

commands_without_state = {
    '/get_income_categories': IncomeCategoryActionsService,
    '/get_expense_categories': ExpenseCategoryActionsService,
}


class UpdatesConsumer:
    """
    Class processes the received messages from the Telegram api and then sent "Event" to EventProcessor
    """

    def __init__(
            self,
            client: BaseClient,
            event_processor: EventProcessor,
            repository: BaseRepository,
    ):
        self._client = client
        self._repository = repository
        self.event_processor = event_processor
        self._last_update_id = 0

    def update_consumer(self, users_state: dict[int: BaseStateMachine]):  # TODO: consume_updates()
        updates = self._client.get_update(self._last_update_id)
        if updates:
            for update in updates:
                event = self._converting_update(update)
                try:
                    users_state = self._check_state_machine(event, users_state)
                except BaseAppError as error:
                    self._client.send_message(event.user.chat_id, error.msg)
        return users_state

    def _converting_update(self, update: dict) -> Event:
        user = User(
            update["message"]["from"]["first_name"],
            update["message"]["chat"]["id"],
        )
        event = Event(
            user,
            update["message"]["text"].strip().lower(),
            update["update_id"]
        )
        self._last_update_id = update["update_id"] + 1
        return event

    def _check_state_machine(
            self, event: Event, users_state: dict[int: BaseStateMachine]
    ) -> dict[int: BaseStateMachine]:  # TODO: rename function
        state_machine = users_state.get(event.user.chat_id)
        if state_machine:
            if event.text == '/cancel':
                users_state[event.user.chat_id] = None
                self._client.send_message(event.user.chat_id, CANCEL_MESSAGE)
            elif state_machine.is_complete():
                users_state[event.user.chat_id] = None
                users_state = self._process_command(event, users_state)
            else:
                state_machine.process(event)
        else:
            users_state = self._process_command(event, users_state)
        return users_state

    def _process_command(self, event: Event, users_state: dict[int: BaseStateMachine]) -> dict[int: BaseStateMachine]:
        command_with_state = commands_with_state.get(event.text)
        if command_with_state:
            state_machine = command_with_state(self._client, self._repository)
            users_state[event.user.chat_id] = state_machine
            state_machine.process(event)
        elif commands_without_state.get(event.text):
            self.event_processor.process(event)
        elif event.text == '/help':
            self._client.send_message(event.user.chat_id, HELP_MESSAGE)
        else:
            self._client.send_message(event.user.chat_id, WRONG_INPUT)
        return users_state
