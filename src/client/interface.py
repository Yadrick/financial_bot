from typing import Protocol


class BaseClient(Protocol):
    def get_update(self, last_update_id: int) -> dict:
        raise NotImplementedError

    def send_message(self, chat_id: str, text: str) -> dict:
        raise NotImplementedError
