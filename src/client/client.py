import requests

from dataclasses import dataclass

from ..client.interface import BaseClient
from ..config.config import API_Link


@dataclass
class ClientInformation:
    first_name: str
    update_id: int
    chat_id: int
    text: str


class TelegramClient(BaseClient):
    """
    Class to communicate with the telegram api
    """
    def __init__(self, api_token: str):
        self.api_token = api_token

    def get_update(self, last_update_id: int):
        updates = requests.get(
            API_Link.format(API_token=self.api_token) + "getUpdates",
            params={
                "offset": last_update_id,
                "timeout": 30,
            },
        ).json()
        return updates["result"]

    def send_message(self, chat_id: int, text: str) -> dict:
        url = API_Link.format(API_token=self.api_token) + "sendMessage"
        data = {"chat_id": str(chat_id), "text": text}
        response = requests.post(url, data=data)
        return response.json()
