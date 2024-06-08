from typing import Optional
from datetime import datetime
from dataclasses import dataclass

from ..app.event import Event
from ..client.interface import BaseClient
from ..errors.app_errors import WrongInputError
from ..repository.interface import BaseRepository
from ..repository.interface_for_transactions_to_save import BaseTransactionInfo
from ..config.config import (
    MESSAGE_ENTER_DATE,
    MESSAGE_ENTER_CATEGORY,
    MESSAGE_ENTER_AMOUNT,
    WRONG_INPUT_DATE,
    WRONG_INPUT_AMOUNT,
    SAVED_RECORD,
)


@dataclass
class IncomeTransactionInfo(BaseTransactionInfo):
    type_category: Optional[str] = 'income'
    first_name: Optional[str] = None
    chat_id: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    amount: Optional[float] = None


class MakeIncomeService:
    """
    Service for making income
    """

    def __init__(self, client: BaseClient, repository: BaseRepository):
        self._client = client
        self._repository = repository
        self._income_tr_info = IncomeTransactionInfo()

    def start_processing(self, event: Event) -> None:
        self._income_tr_info.chat_id = event.user.chat_id
        self._income_tr_info.first_name = event.user.first_name
        categories = self._repository.get_categories(
            self._income_tr_info.type_category, self._income_tr_info.chat_id
        )
        self._client.send_message(
            self._income_tr_info.chat_id, MESSAGE_ENTER_CATEGORY + str(categories)
        )

    def category_processing(self, event: Event) -> None:
        self._income_tr_info.category = event.text.capitalize()
        self._client.send_message(self._income_tr_info.chat_id, MESSAGE_ENTER_DATE)

    def date_processing(self, event: Event) -> None:
        try:
            date = datetime.strptime(event.text, "%d-%m-%Y")
            self._income_tr_info.date = date
            self._client.send_message(self._income_tr_info.chat_id, MESSAGE_ENTER_AMOUNT)
        except ValueError:
            raise WrongInputError(WRONG_INPUT_DATE)

    def amount_processing(self, event: Event) -> None:
        try:
            self._income_tr_info.amount = float(event.text)
            self._repository.save(self._income_tr_info)

            message = SAVED_RECORD.format(
                category=self._income_tr_info.category,
                date=self._income_tr_info.date.strftime("%d-%m-%Y"),
                amount=self._income_tr_info.amount,
            )
            self._client.send_message(self._income_tr_info.chat_id, message)
        except ValueError:
            raise WrongInputError(WRONG_INPUT_AMOUNT)
