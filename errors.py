class InvalidCardError(Exception):

    def __init__(self, message="Cannot play this card"):
        self.message = message
        super().__init__(self.message)