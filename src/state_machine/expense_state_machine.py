from enum import Enum, auto
from typing import Callable, Dict

from .interface import BaseStateMachine
from ..app.event import Event
from ..services.expense_service import MakeExpenseService
from ..services.income_service import MakeIncomeService
from ..client.interface import BaseClient
from ..repository.interface import BaseRepository


class State(Enum):
    START = auto()
    RECEIVED_CATEGORY = auto()
    RECEIVED_DATE = auto()
    RECEIVED_AMOUNT = auto()
    END = auto()


_mapping = {
    State.START: State.RECEIVED_CATEGORY,
    State.RECEIVED_CATEGORY: State.RECEIVED_DATE,
    State.RECEIVED_DATE: State.RECEIVED_AMOUNT,
    State.RECEIVED_AMOUNT: State.END
}


class ExpenseStateMachine(BaseStateMachine):
    def __init__(self, client: BaseClient, repository: BaseRepository):
        self._expense_service = MakeExpenseService(client, repository)
        self._action_for_state: Dict[State, Callable[[Event], None]] = {
            State.START: self._expense_service.start_processing,
            State.RECEIVED_CATEGORY: self._expense_service.category_processing,
            State.RECEIVED_DATE: self._expense_service.date_processing,
            State.RECEIVED_AMOUNT: self._expense_service.amount_processing,
        }
        self._state = State.START

    def current_state(self) -> State:
        return self._state

    def is_complete(self) -> bool:
        return True if self._state == State.END else False

    def _go_next_state(self) -> None:
        self._state = _mapping.get(self._state)

    def process(self, event: Event) -> None:
        self.state_resolver(event)
        self._go_next_state()

    def state_resolver(self, event: Event) -> None:
        action = self._action_for_state.get(self._state)
        action(event)
