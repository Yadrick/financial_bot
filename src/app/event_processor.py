from typing import Dict, Callable

from .event import Event
from ..client.interface import BaseClient
from ..errors.app_errors import BaseAppError
from ..services.category_service import CategoryActionsService


commands = {
    '/get_income_categories': CategoryActionsService.get_income_categories,
    '/get_expense_categories': CategoryActionsService.get_expense_categories,
    '/delete_income_categories': CategoryActionsService.delete_income_categories,
    '/delete_expense_categories': CategoryActionsService.delete_expense_categories,
}


class EventProcessor:
    """
    Class processes the received messages from the Telegram api and then launches the necessary services
    """

    def __init__(self, client: BaseClient, category_service: CategoryActionsService):
        self.client = client
        self.commands: Dict[str, Callable[[Event], None]] ={
            '/get_income_categories': category_service.get_income_categories,
            '/get_expense_categories': category_service.get_expense_categories,
            '/delete_income_categories': category_service.delete_income_categories,
            '/delete_expense_categories': category_service.delete_expense_categories,
        }

    def process(self, event: Event) -> None:
        try:
            command = self.commands.get(event.text)
            command(event)
        except BaseAppError as error:
            self.client.send_message(event.user.chat_id, error.msg)
