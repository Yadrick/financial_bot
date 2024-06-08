from enum import Enum
from typing import Protocol

from ..app.event import Event


class BaseStateMachine(Protocol):
    """
    Class for storing and updating client state
    """

    def is_complete(self) -> bool:
        raise NotImplementedError

    def _go_next_state(self) -> None:
        raise NotImplementedError

    def process(self, event: Event) -> None:
        raise NotImplementedError

    def _state_resolver(self, event: Event) -> None:
        raise NotImplementedError
