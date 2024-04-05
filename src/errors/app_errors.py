class BaseAppError(Exception):
    def __init__(self, msg: str = ''):
        self.msg = msg
        super().__init__(self.msg)


class WrongInputError(BaseAppError):
    pass
