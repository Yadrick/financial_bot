from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .machine_state import StateMachine
from ..app.machine_commands import CommandsMachine


@dataclass
class ClientLastInfo:
    """
    Class for storing user data information
    """
    chat_id: int
    category: Optional[str] = None
    date: Optional[datetime] = None
    amount: Optional[float] = None
    family: Optional[str] = None


@dataclass
class ClientStateInfo:
    """
    Class for storing information about the status of the process of receiving data from the user
    """
    state: StateMachine
    command: CommandsMachine
    last_info: ClientLastInfo