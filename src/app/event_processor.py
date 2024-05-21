from .update_consumer import User
from ..app.machine_state import State
from ..client.interface import BaseClient
from ..app.machine_commands import Commands
from ..errors.app_errors import BaseAppError
from ..services.income_service import MakeIncomeService
from ..app.client_info import UserStateInfo, UserLastInfo
from ..services.expense_service import MakeExpenseService
from ..services.category_service import CategoryActionsService
from ..config.config import STARTING_MESSAGE, WRONG_INPUT, CANCEL_MESSAGE


class EventProcessor:
    """
    Class processes the received messages from the Telegram api and then launches the necessary services
    """

    def __init__(
        self,
        client: BaseClient,
        income_service: MakeIncomeService,
        expense_service: MakeExpenseService,
        category_service: CategoryActionsService,
    ):
        self.client = client
        self.income_service = income_service
        self.expense_service = expense_service
        self.category_service = category_service

    def processing(
            self,
            user: User,
            user_state_info: UserStateInfo,
            users: dict[str: UserStateInfo],
    ) -> dict[str: UserStateInfo]:
        try:
            if user.text in ("/start", "/help"):
                user_state_info.state.change_state(State.START)
                user_state_info.command.change_command(Commands.NONE)
                user_state_info.last_info = UserLastInfo(
                    user.chat_id
                )
                self.client.send_message(
                    user.chat_id, STARTING_MESSAGE
                )
            elif user.text == "/cancel":
                user_state_info.state.change_state(State.START)
                user_state_info.command.change_command(Commands.NONE)
                user_state_info.last_info = UserLastInfo(
                    user.chat_id
                )
                self.client.send_message(
                    user.chat_id, CANCEL_MESSAGE
                )
            elif (
                user.text == "/make_income" or
                user_state_info.command.current_command == Commands.MAKE_INCOME
            ):
                user_state_info = self.income_service.make_income(
                    user, user_state_info
                )
                users[user.chat_id] = user_state_info
            elif (
                user.text == "/make_expense"
                or user_state_info.command.current_command
                == Commands.MAKE_EXPENSE
            ):
                user_state_info = self.expense_service.make_expense(
                    user, user_state_info
                )
                users[user.chat_id] = user_state_info
            elif user.text == "/get_income_categories":
                user_state_info = self.category_service.get_income_categories(
                    user, user_state_info
                )
                users[user.chat_id] = user_state_info
            elif user.text == "/get_expense_categories":
                user_state_info = (
                    self.category_service.get_expense_categories(
                        user, user_state_info
                    )
                )
                users[user.chat_id] = user_state_info
            elif (
                user.text == "/delete_income_categories"
                or user_state_info.command.current_command
                == Commands.DELETE_INCOME_CATEGORIES
            ):
                user_state_info = (
                    self.income_service.delete_income_categories(
                        user, user_state_info
                    )
                )
                users[user.chat_id] = user_state_info
            elif (
                user.text == "/delete_expense_categories"
                or user_state_info.command.current_command
                == Commands.DELETE_EXPENSE_CATEGORIES
            ):
                user_state_info = (
                    self.expense_service.delete_expense_categories(
                        user, user_state_info
                    )
                )
                users[user.chat_id] = user_state_info
            else:
                self.client.send_message(user.chat_id, WRONG_INPUT)

            return users
        except BaseAppError as error:
            self.client.send_message(user.chat_id, error.msg)
