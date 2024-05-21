from .update_consumer import UpdatesConsumer


class TelegramBotApp:
    """
    Class to launch the bot
    """
    def __init__(self, updates_consumer: UpdatesConsumer):
        self.updates_consumer = updates_consumer

    def start(self):
        users = {}
        while True:
            users = self.updates_consumer.update_consumer(users)
