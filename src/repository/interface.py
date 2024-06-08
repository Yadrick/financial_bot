from typing import Protocol

from .categories import Categories
from .interface_for_transactions_to_save import BaseTransactionInfo
from ..app.event import Event


class BaseRepository(Protocol):

    def save_user(self, event: Event):
        raise NotImplementedError

    def save_category(self, event: Event, type_category: str):
        raise NotImplementedError

    def save(self, transaction_info: BaseTransactionInfo):
        raise NotImplementedError

    def get_categories(self, type_category: str, chat_id: str) -> Categories:
        raise NotImplementedError

    def delete_category_and_related_transactions(self, event: Event, type_category: str):
        raise NotImplementedError
