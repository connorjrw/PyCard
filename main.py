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

    def deal(self, deal_count=52):
        playerNum = 0
        playerNumLength = len(self._players)
        if deal_count != 52:
            deal_count = deal_count * len(self._players)
        for card in self._deck.deck[:deal_count]:
            self._players[playerNum].addToHand(card)
            playerNum = playerNum + 1
            self._deck.removeCard(card)
            if playerNum >= playerNumLength:
                playerNum = 0

    def dealToPlayer(self, player, cards):
        if cards > len(self._deck.deck):  # if nothing left to deal, deal the rest of the pack
            cards = len(self._deck.deck)
        dealt_cards = self._deck.deck[:cards]
        player.addMultipleToHand(dealt_cards)
        self._deck.removeMultipleCards(dealt_cards)


class Player:
    def __init__(self, name):
        self._name = name
        self._hand = []

    def addToHand(self, card):
        self._hand.append(card)

    def addMultipleToHand(self, cards):
        for card in cards:
            self._hand.append(card)

    def removeFromHand(self, card):
        self._hand.remove(card)

    def handAsStringList(self):
        cardList = []
        for card in self._hand:
            cardList.append(card.cardAsString())
        return cardList

    def playCard(self, card, stack):
        stack.addToStack(card)
        self._hand.remove(card)

    @property
    def hand(self):
        return self._hand

    def name(self):
        return self._name


class Stack:
    def __init__(self):
        self._active = False
        self._stack = []

    def addToStack(self, card):
        self._stack.append(card)

    @property
    def stack(self):
        return self._stack


class Game:

    def __init__(self, players):
        self._players = players
        self._playerTurn = players[0]

    def setPlayerTurn(self, player):
        self._playerTurn = player

    def setNextPlayerTurn(self):
        currentTurn = self._players.index(self._playerTurn) + 1
        if currentTurn == len(self._players):
            currentTurn = 0
        self._playerTurn = self._players[currentTurn]

    @property
    def playerTurn(self):
        return self._playerTurn


class Deck:
    def __init__(self):
        self._deck = self.create()

    def create(self):
        suits = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
        values = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
        deck = []
        for suit in suits:
            for value in values:
                currentCard = Card(suit, value)
                deck.append(currentCard)
        return deck

    def removeCard(self, cardToRemove):
        for index, card in enumerate(self._deck):
            if cardToRemove == card:
                del self._deck[index]

    def removeMultipleCards(self, cardsToRemove):
        for index, card in enumerate(self._deck[:]):
            if card in cardsToRemove:
                self._deck.remove(card)

    def shuffle(self):
        random.shuffle(self._deck)

    @property
    def deck(self):
        return self._deck

# class Game:


if __name__ == '__main__':
    # newCard = Card('hearts', 'ace')
    newDeck = Deck()
    newDeck.shuffle()
    player1 = Player()
    player2 = Player()
    players = [player1, player2]
    dealer = Dealer(newDeck, players)

    dealer.deal()


