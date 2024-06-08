from ..app.event import Event
from ..repository.interface import BaseRepository
from ..client.interface import BaseClient
from ..config.config import MESSAGE_SHOW_INCOME_CATEGORY
from ..config.config import (
    DELETE_INCOME_CATEGORY_MESSAGE,
    CATEGORY_SUCCESSFULLY_DELETED,
    CATEGORY_NOT_DELETED,
    CATEGORIES_NOT_FOUND,
)


class IncomeCategoryActionsService:
    def __init__(self, client: BaseClient, repository: BaseRepository):
        self._client = client
        self._repository = repository
        self._type_category_income = 'income'
        self._chat_id = ''

    def start_processing(self, event: Event) -> None:
        self._chat_id = event.user.chat_id
        categories = self._repository.get_categories(
            self._type_category_income, self._chat_id
        )
        if categories:
            self._client.send_message(
                self._chat_id,
                DELETE_INCOME_CATEGORY_MESSAGE + str(categories),
            )
        else:
            self._client.send_message(
                self._chat_id,
                CATEGORIES_NOT_FOUND,
            )

    def get_income_categories(self, event: Event) -> None:
        categories = self._repository.get_categories(
            self._type_category_income, event.user.chat_id
        )
        self._client.send_message(
            event.user.chat_id, MESSAGE_SHOW_INCOME_CATEGORY + str(categories)
        )
        self._repository.save_user(event)

    def delete_income_categories(self, event: Event) -> None:
        event.text = event.text.capitalize()
        result = self._repository.delete_category_and_related_transactions(
            event, self._type_category_income
        )
        if result:
            self._client.send_message(
                self._chat_id, CATEGORY_SUCCESSFULLY_DELETED
            )
        else:
            self._client.send_message(
                self._chat_id, CATEGORY_NOT_DELETED
            )
