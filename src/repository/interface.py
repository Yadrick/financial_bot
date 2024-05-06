from typing import Protocol

from .categories import Categories
from ..app.client_info import ClientLastInfo


class BaseRepository(Protocol):

    def save_user(self, last_info: ClientLastInfo):
        raise NotImplementedError

    def save_category(self, last_info: ClientLastInfo, type_category: str):
        raise NotImplementedError

    def save_transaction(self, last_info: ClientLastInfo, type_category: str):
        raise NotImplementedError

    def get_categories(self, type_category: str, chat_id: str) -> Categories:
        raise NotImplementedError

    def delete_category_and_related_transactions(self, last_info: ClientLastInfo):
        raise NotImplementedError
