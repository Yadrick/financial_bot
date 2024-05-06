import pytest

from ..src.app.client_info import ClientStateInfo, ClientLastInfo, ClientInformation
from ..src.app.machine_commands import CommandsMachine
from ..src.app.machine_state import StateMachine
from ..src.repository.categories import Categories


@pytest.fixture
def client_information() -> ClientInformation:
    client_information = ClientInformation(
        first_name="John",
        update_id=12345,
        chat_id=67890,
        text="Test message"
    )
    return client_information


@pytest.fixture
def client_state_info() -> ClientStateInfo:
    client_state_info = ClientStateInfo(
        StateMachine(),
        CommandsMachine(),
        ClientLastInfo(chat_id=67890)
    )
    return client_state_info


@pytest.fixture
def categories() -> Categories:
    categories = Categories(
        ['Продукты', 'Кафе', 'Налоги']
    )
    return categories
