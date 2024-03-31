from typing import Protocol


class BaseClient(Protocol):
    def get_update(self, last_update_id: int):
        raise NotImplemented

    def send_message(self, chat_id: int, text: str) -> dict:
        raise NotImplemented
