from typing import Protocol


class BaseRepository(Protocol):
    def save(self, last_info: dict):
        raise NotImplementedError

    def get_categories(self) -> list[str]:
        raise NotImplementedError
