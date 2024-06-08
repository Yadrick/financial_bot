from typing import Protocol


class BaseClient(Protocol):
    def get_update(self, last_update_id: int) -> dict:
        raise NotImplementedError

    def send_message(self, chat_id: int, text: str) -> dict:
        raise NotImplementedError

    def send_photo(self, chat_id: int, photo_path):
        raise NotImplementedError
