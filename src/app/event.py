from typing import Optional
from datetime import datetime
from dataclasses import dataclass

from ..state_machine.interface import BaseStateMachine


@dataclass
class User:
    """
    Class for storing user information
    """

    first_name: str
    update_id: int
    chat_id: int
    text: str


@dataclass
class UserLastInfo:
    """
    Class for storing last user information
    """

    chat_id: int
    name: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    amount: Optional[float] = None
    family: Optional[str] = None


@dataclass
class Event:
    """
    Class for storing event information
    """

    user: User
    user_last_info: UserLastInfo
    command: bool
    state_machine: BaseStateMachine | None
