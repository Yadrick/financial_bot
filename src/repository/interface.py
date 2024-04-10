from typing import Protocol

from .categories import Categories
from ..app.commander import ClientLastInfo


class BaseRepository(Protocol):
    def save(self, last_info: ClientLastInfo, type_category: str):
        raise NotImplementedError

    def get_categories(self, type_category: str, chat_id: str) -> Categories:
        raise NotImplementedError
