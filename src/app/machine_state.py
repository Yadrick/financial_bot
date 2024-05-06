from enum import Enum, auto


class State(Enum):
    START = auto()
    RECEIVED_CATEGORY = auto()
    RECEIVED_DATE = auto()
    RECEIVED_AMOUNT = auto()
    WAITING_CATEGORY = auto()


class StateMachine:
    """
    Class for storing and updating client state
    """

    def __init__(self):
        self.current_state = State.START

    def change_state(self, new_state: State):
        self.current_state = new_state
