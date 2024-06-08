from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    chat_id: str


@dataclass
class Event:
    user: User
    text: str
    update_id: str
