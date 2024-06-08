from ..repository.interface import BaseRepository
from ..client.interface import BaseClient
from ..app.client_info import ClientStateInfo, ClientInformation
from ..config.config import MESSAGE_SHOW_INCOME_CATEGORY, MESSAGE_SHOW_EXPENSE_CATEGORY


class CategoryActionsService:

    def __init__(self, client: BaseClient, repository: BaseRepository):
        self.client = client
        self.repository = repository
        self.type_category_income = "income"
        self.type_category_expense = "expense"

    def get_income_categories(
        self, client_information: ClientInformation, client_state_info: ClientStateInfo
    ):
        client_state_info.last_info.chat_id = client_information.chat_id
        client_state_info.last_info.name = client_information.first_name
        categories = self.repository.get_categories(
            self.type_category_income, client_state_info.last_info.chat_id
        )
        self.client.send_message(
            client_information.chat_id, MESSAGE_SHOW_INCOME_CATEGORY + str(categories)
        )
        self.repository.save_user(client_state_info.last_info)
        return client_state_info

    def get_expense_categories(
        self, client_information: ClientInformation, client_state_info: ClientStateInfo
    ):
        client_state_info.last_info.chat_id = client_information.chat_id
        client_state_info.last_info.name = client_information.first_name
        categories = self.repository.get_categories(
            self.type_category_expense, client_state_info.last_info.chat_id
        )
        self.client.send_message(
            client_information.chat_id, MESSAGE_SHOW_EXPENSE_CATEGORY + str(categories)
        )
        self.repository.save_user(client_state_info.last_info)
        return client_state_info
