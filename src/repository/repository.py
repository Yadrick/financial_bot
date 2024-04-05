from ..repository.interface import BaseRepository


class PostgreSQLRepository(BaseRepository):
    """
    Class for communication with PostgreSQL
    """
    def __init__(self):
        pass

    def save(self, last_info: dict):
        pass

    def get_categories(self) -> list[str]:
        return ['продукты', 'кафе', 'налоги']
