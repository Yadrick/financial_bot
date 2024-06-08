from ..repository.interface import BaseRepository
from ..client.interface import BaseClient
from ..app.client_info import ClientStateInfo, ClientInformation
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
import locale

sns.set()


locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian",
)


class ReportService:
    def __init__(self, client: BaseClient, repository: BaseRepository):
        self.client = client
        self.repository = repository

    def report_per_day(
        self, client_information: ClientInformation, client_state_info: ClientStateInfo
    ):
        client_state_info.last_info.chat_id = client_information.chat_id
        client_state_info.last_info.name = client_information.first_name
        result = self.repository.report_per_day(client_information.chat_id)
        print(result)
        self.plot_report(result, f"Отчет за {date.today()}", client_information)
        return client_state_info

    def report_per_month(
        self, client_information: ClientInformation, client_state_info: ClientStateInfo
    ):
        client_state_info.last_info.chat_id = client_information.chat_id
        client_state_info.last_info.name = client_information.first_name
        result = self.repository.report_per_month(client_information.chat_id)
        print(result)
        self.plot_report(
            result,
            f"Отчет за месяц {date.today().strftime('%B %Y')}",
            client_information,
        )
        return client_state_info

    def plot_report(
        self, data: list[tuple], title: str, client_information: ClientInformation
    ):
        categories = [item[0] for item in data]
        amounts = [item[1] for item in data]
        plt.figure(figsize=(10, 6))
        colors = ["#aec6cf", "#ffb3ba"]
        plt.bar(categories, amounts, color=colors)
        plt.xlabel("Категории")
        plt.ylabel("Сумма")
        plt.title(title)
        plt.tight_layout()

        plot_path = "plot.png"
        plt.savefig(plot_path)

        self.client.send_photo(client_information.chat_id, plot_path)
