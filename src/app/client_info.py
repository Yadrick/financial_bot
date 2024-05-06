from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .machine_state import StateMachine
from ..app.machine_commands import CommandsMachine


@dataclass
class ClientInformation:
    first_name: str
    update_id: int
    chat_id: int
    text: str


@dataclass
class ClientLastInfo:
    """
    Class for storing user data information
    """

    chat_id: int
    name: Optional[str] = None
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
