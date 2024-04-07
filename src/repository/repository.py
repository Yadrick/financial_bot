from .categories import Categories
from ..app.client_info import ClientLastInfo
from ..repository.interface import BaseRepository


class PostgreSQLRepository(BaseRepository):
    """
    Class for communication with PostgreSQL
    """
    def __init__(self):
        pass

    def save(self, last_info: ClientLastInfo):
        pass

    def get_categories(self) -> Categories:
        return Categories(['Продукты', 'Кафе', 'Налоги'])
