import random


class Card:
    def __init__(self, suit, value):
        self._suit = suit
        self._value = value

    @property
    def suit(self):
        return self._suit

    @property
    def value(self):
        return self._value

    def cardAsString(self):
        return self.value + ' of ' + self.suit


class Dealer:
    def __init__(self, deck, players):
        self._deck = deck
        self._players = players

    def deal(self):
        playerNum = 0
        playerNumLength = len(players)
        for card in self._deck.deck:
            players[playerNum].addToHand(card)
            playerNum = playerNum + 1
            if playerNum >= playerNumLength:
                playerNum = 0


class Player:
    def __init__(self):
        self._hand = []

    def addToHand(self, card):
        self._hand.append(card)

    def handAsStringList(self):
        cardList = []
        for card in self._hand:
            cardList.append(card.cardAsString())
        return cardList
    @property
    def hand(self):
        return self._hand


class Deck:
    def __init__(self):
        self._deck = self.create()

    def create(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
        deck = []
        for suit in suits:
            for value in values:
                currentCard = Card(suit, value)
                deck.append(currentCard)
        return deck

    def shuffle(self):
        random.shuffle(self._deck)

    @property
    def deck(self):
        return self._deck


if __name__ == '__main__':
    # newCard = Card('hearts', 'ace')
    newDeck = Deck()
    newDeck.shuffle()
    player1 = Player()
    player2 = Player()
    players = [player1, player2]
    dealer = Dealer(newDeck, players)

    dealer.deal()
    # print(newDeck)
    # print(player5.handAsStringList())x
    print(player2.hand[0].cardAsString())
    # print(newDeck.deck[2].cardAsString())


