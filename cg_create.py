import random
from _ast import Raise

from errors import *


class Card:
    def __init__(self, suit, value):
        self._suit = suit
        self._value = value

    def card_name(self):
        return self._value + ' of ' + self._suit

    @property
    def suit(self):
        return self._suit

    @property
    def value(self):
        return self._value

    @suit.setter
    def suit(self, suit):
        self._suit = suit

    @value.setter
    def value(self, value):
        self._value = value


class Dealer:
    def __init__(self, deck, players):
        self._deck = deck
        self._players = players

    def deal(self, card_count=52):
        # card_count takes amount of cards per player, then multiplies by number of players
        # Deals all cards if not provided
        cp_index = 0
        ttl_players = len(self._players)
        if card_count != 52:
            card_count = card_count * len(self._players)
        for card in self._deck.deck[:card_count]:
            self._players[cp_index].add_to_hand(card)
            cp_index += 1
            self._deck.remove_card(card)
            if cp_index >= ttl_players:
                cp_index = 0

    def deal_to_player(self, player, cards):
        if cards > len(self._deck.deck):  # if nothing left to deal, deal the rest of the pack
            cards = len(self._deck.deck)
        dealt_cards = self._deck.deck[:cards]
        player.add_multiple_to_hand(dealt_cards)
        self._deck.remove_multiple_cards(dealt_cards)

    def shuffle_deck(self):
        self._deck.shuffle()


class Player:
    def __init__(self, name):
        self._name = name
        self._hand = []

    def add_to_hand(self, card):
        self._hand.append(card)

    def add_multiple_to_hand(self, cards):
        for card in cards:
            self._hand.append(card)

    def remove_from_hand(self, card):
        self._hand.remove(card)

    def handAsStringList(self):
        cardList = ""
        for card in self._hand:
            cardList = cardList + (card.card_name()) + ', '
        return cardList

    def card_list_string(self):
        cardList = []
        for card in self._hand:
            cardList.append(card.card_name())
        return cardList

    def playCard(self, card, stack):
        stack.addToStack(card)
        self._hand.remove(card)

    def get_card(self, card_name):
        return self._hand[self.card_list_string().index(card_name)]

    def set_hand(self, hand):
        self._hand = hand

    @property
    def hand(self):
        return self._hand

    def name(self):
        return self._name


class Stack:
    def __init__(self, stack_rules=None):
        self._active = False
        self._stack = []
        self._stack_rules = stack_rules

    def addToStack(self, card):
        if self.validate_move(card):
            self._stack.append(card)
        else:
            raise InvalidCardError()

    @property
    def stack(self):
        return self._stack

    def top_card(self):
        if len(self._stack) == 0:
            return None
        else:
            return self._stack[len(self._stack) - 1]

    def validate_suit(self, card):
        if card.suit in self._stack_rules['Suits'][self.top_card().suit]:
            return (self._stack_rules['Suits'][self.top_card().suit][card.suit],
                    self._stack_rules['Suits'][self.top_card().suit]['Enforced'])
        else:
            return self._stack_rules['Suits'][self.top_card().suit]['Default'], False

    def validate_value(self, card):
        print('value', card.value, self._stack_rules['Values'][self.top_card().value])
        if card.value in self._stack_rules['Values'][self.top_card().value]:
            return (self._stack_rules['Values'][self.top_card().value][card.value],
                    self._stack_rules['Values'][self.top_card().value]['Enforced'])
        else:
            return (self._stack_rules['Values'][self.top_card().value]['Default'],
                    self._stack_rules['Values'][self.top_card().value]['Enforced'])

    def validate_move(self, card):
        if self.top_card() is None:
            if card.suit in self._stack_rules['None']:
                # Further validation
                suit = self._stack_rules['None'][card.suit]
            else:
                return self._stack_rules['None']['Default']
        else:
            v_suit = self.validate_suit(card)
            v_value = self.validate_value(card)
            print(v_suit, v_value)
            if v_suit[1] and v_value[1]:  # Both Enforced
                return v_suit[0] and v_value[0]
            elif v_suit[1] and not v_value[1]:  # Suit is Enforced
                return v_suit[0]
            elif not v_suit[1] and v_value[1]:  # Value is Enforced
                return v_value[0]
            elif not v_suit[1] and not v_value[1]:  # Nothing is enforced
                return v_value[0] or v_suit[0]
        # if self.top_card() is None:
        #     return True
        # else:
        #     if self._stack_order.index(card.value) > self._stack_order.index(self.top_card().value):
        #         return True
        #     else:
        #         return False


class Game:

    def __init__(self, players):
        self._players = players
        self._player_turn = players[0]

    def set_player_turn(self, player):
        self._player_turn = player

    def set_next_player_turn(self):
        currentTurn = self._players.index(self._player_turn) + 1
        if currentTurn == len(self._players):
            currentTurn = 0
        self._player_turn = self._players[currentTurn]

    @property
    def player_turn(self):
        return self._player_turn


class Deck:
    def __init__(self):
        self._deck = self.create()

    def create(self):
        suits = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
        values = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six',
                  'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
        deck = []
        for suit in suits:
            for value in values:
                current_card = Card(suit, value)
                deck.append(current_card)
        return deck

    def remove_card(self, card_to_remove):
        for index, card in enumerate(self._deck):
            if card_to_remove == card:
                del self._deck[index]

    def remove_multiple_cards(self, cards_to_remove):
        for index, card in enumerate(self._deck[:]):
            if card in cards_to_remove:
                self._deck.remove(card)

    def shuffle(self):
        random.shuffle(self._deck)

    @property
    def deck(self):
        return self._deck
