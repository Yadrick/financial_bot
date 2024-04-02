from enum import Enum, auto


class Commands(Enum):
    NONE = auto()
    MAKE_INCOME = auto()
    MAKE_EXPENSE = auto()
    GET_INCOME_CATEGORIES = auto()
    GET_EXPENSE_CATEGORIES = auto()
    DELETE_INCOME_CATEGORIES = auto()
    DELETE_EXPENSE_CATEGORIES = auto()
    REPORT_PER_DAY = auto()
    REPORT_PER_MONTH = auto()
    REPORT_PER_PERIOD = auto()


class CommandsMachine:
    """
    Class for storing and updating client state
    """

    def __init__(self):
        self.current_command = Commands.NONE

    def change_command(self, new_comand: Commands):
        self.current_command = new_comand
