from enum import Enum
from typing import Protocol


class BaseStateMachine(Protocol):
    """
    Class for storing and updating client state
    """

    def get_state(self) -> Enum:
        raise NotImplementedError

    def go_next_state(self) -> None:
        raise NotImplementedError

    def is_on(self) -> bool:
        raise NotImplementedError
