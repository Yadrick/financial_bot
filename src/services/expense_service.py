from client.machine_state import StateMachine, State
from client.client import Client


class ExpenseService:

    def __init__(self) -> None:
        self.state_machine = StateMachine()
        self.client = Client()
        self.data = {}

    def execute(self):

        while True:
            self.client_updates = self.client.get_updates()
            if (
                self.client_updates["text"] == "/cancel"
                or self.state_machine.current_state == State.FINISH
            ):
                break

            if self.state_machine.current_state == State.START:
                self.client.send_mesage("Введите то-то")

                self.state_machine.change_state(State.RECEIVED_AMOUNT)
            if self.state_machine.current_state == State.RECEIVED_AMOUNT:
                self.data["category"] = self.client_updates["text"]
                self.client.send_mesage("Введите дату")

                self.state_machine.change_state(State.RECEIVED_DATE)
            if self.state_machine.current_state == State.RECEIVED_DATE:
                self.data["date"] = self.client_updates["text"]
                self.client.send_mesage("Введите сумму")

                self.state_machine.change_state(State.RECEIVED_AMOUNT)
            if self.state_machine.current_state == State.RECEIVED_AMOUNT:
                self.data["amount"] = self.client_updates["text"]
                self.client.send_mesage("Вот ваша запись: ")

                self.state_machine.change_state(State.FINISH)
                self.database.save(self.data)
