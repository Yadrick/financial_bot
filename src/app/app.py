from ..app.commander import Commander


class TelegramBotApp:
    """
    Class to launch the bot
    """
    def __init__(self, commander: Commander):
        self.commander = commander

    def start(self):
        clients = {}
        while True:
            clients = self.commander.manage(clients)
