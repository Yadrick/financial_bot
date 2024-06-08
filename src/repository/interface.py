from typing import Protocol

from .categories import Categories
from ..app.client_info import ClientLastInfo


class BaseRepository(Protocol):

    def save(self, last_info: ClientLastInfo, type_category: str):
        raise NotImplementedError

    def save_user(self, last_info: ClientLastInfo):
        raise NotImplementedError

    def get_categories(self, type_category: str, chat_id: str) -> Categories:
        raise NotImplementedError

    def delete_category_and_related_transactions(self, last_info: ClientLastInfo):
        raise NotImplementedError

    def report_per_day(self, chat_id: str):
        raise NotImplementedError

    def report_per_month(self, chat_id: str):
        raise NotImplementedError
