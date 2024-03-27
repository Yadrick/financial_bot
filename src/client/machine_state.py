from enum import Enum, auto


class State(Enum):
    START = auto()
    RECEIVED_CATEGORY = auto()
    RECEIVED_DATE = auto()
    RECEIVED_AMOUNT = auto()
    FINISH = auto()
    # далее можно список дополнить необходимыми состояниями


class StateMachine:
    def __init__(self):
        self.current_state = State.START

    def change_state(self, new_state):
        self.current_state = new_state
