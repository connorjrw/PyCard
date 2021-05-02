class InvalidCardError(Exception):

    def __init__(self, message="Cannot play this card"):
        self.message = message
        super().__init__(self.message)


class InvalidTurnError(Exception):
    def __init__(self, message="Not this Players Turn"):
        self.message = message
        super().__init__(self.message)


class CardNotInHandError(Exception):
    def __init__(self, message="Card is not in players hand"):
        self.message = message
        super().__init__(self.message)
