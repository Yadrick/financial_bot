from typing import Protocol

from .categories import Categories
from ..app.client_info import ClientLastInfo


class BaseRepository(Protocol):
    def save(self, last_info: ClientLastInfo):
        raise NotImplementedError

    def get_categories(self) -> Categories:
        raise NotImplementedError
