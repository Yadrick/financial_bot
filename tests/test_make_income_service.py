import mock

from financial_bot.src.repository.interface import BaseRepository
from financial_bot.tests.fixture import client_information, client_state_info, categories
from financial_bot.src.app.client_info import ClientStateInfo, ClientInformation
from financial_bot.src.app.machine_commands import Commands
from financial_bot.src.app.machine_state import State
from financial_bot.src.client.interface import BaseClient
from financial_bot.src.repository.categories import Categories
from financial_bot.src.services.income_service import MakeIncomeService


def test_start_processing(
        client_information: ClientInformation,
        client_state_info: ClientStateInfo,
        categories: Categories
):
    client = mock.create_autospec(BaseClient, instance=True)
    repository = mock.create_autospec(BaseRepository, instance=True)
    repository.get_categories = mock.MagicMock(return_value=categories)
    make_income_service = MakeIncomeService(client, repository)

    make_income_service.make_income(client_information, client_state_info)

    assert client_state_info.state.current_state == State.RECEIVED_CATEGORY
    assert client_state_info.command.current_command == Commands.MAKE_INCOME
