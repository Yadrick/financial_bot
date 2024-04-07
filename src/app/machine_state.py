from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum, auto

from ..app.machine_commands import CommandsMachine


class State(Enum):
    START = auto()
    RECEIVED_CATEGORY = auto()
    RECEIVED_DATE = auto()
    RECEIVED_AMOUNT = auto()


class StateMachine:
    """
    Class for storing and updating client state
    """

    def __init__(self):
        self.current_state = State.START

    def change_state(self, new_state: State):
        self.current_state = new_state


@dataclass
class ClientLastInfo:
    category: Optional[str] = None
    date: Optional[datetime] = None
    amount: Optional[float] = None
    family: Optional[str] = None
    chat_id: Optional[str] = None


@dataclass
class ClientStateInfo:
    state: StateMachine
    command: CommandsMachine
    last_info: ClientLastInfo
