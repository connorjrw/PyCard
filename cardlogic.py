import random
import pygame
from _ast import Raise

from errors import *


class Card:
    def __init__(self, suit, value):
        self._suit = suit
        self._value = value
        self._rect = pygame.Rect(0, 0, 0, 0)
        self._image = 'images/Cards/' + suit + value + '.png'
        self._is_moved = False
        self._position = [-1, -1]
        self._previous_position = []

    def set_previous_position(self, position):
        self._previous_position = position

    def get_previous_position(self):
        return self._previous_position

    def card_name(self):
        return self._value + ' of ' + self._suit

    def is_moved(self):
        return self._is_moved

    def set_moved(self, position):
        self._is_moved = True

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position
        self.set_card_rect([position[0], position[1], 84, 114])

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

    def display_card(self, display, location):
        card_img = pygame.image.load(self._image)
        card_img = pygame.transform.scale(card_img, (84, 114))
        display.blit(card_img, ([location[0], location[1]]))

    def set_card_rect(self, position):
        self._rect = pygame.Rect(position[0], position[1], position[2], position[3])

    def get_card_rect(self):
        return self._rect


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
        for card in self._deck.deck()[:card_count]:
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
    def __init__(self, name, location):
        self._name = name
        self._hand = []
        self._x = location[0]
        self._y = location[1]

    def add_to_hand(self, card):
        self._hand.append(card)
        self.set_hand_positions()

    def add_multiple_to_hand(self, cards):
        for card in cards:
            self._hand.append(card)

    def remove_from_hand(self, card):
        if card in self._hand:
            self._hand.remove(card)
            self.set_hand_positions()
        else:
            raise CardNotInHandError()

    def hand_as_string(self):
        cardList = ""
        for card in self._hand:
            cardList = cardList + (card.card_name()) + ', '
        return cardList

    def card_list_string(self):
        cardList = []
        for card in self._hand:
            cardList.append(card.card_name())
        return cardList

    def get_card_in_hand(self, card_string):  # Untested
        for card in self._hand:
            if card.card_name() == card_string:
                return card
        raise CardNotInHandError()

    def play_card(self, card, stack):
        stack.add_to_stack(card)
        self.remove_from_hand(card)

    def get_card(self, card_name):
        return self._hand[self.card_list_string().index(card_name)]

    def set_hand(self, hand):
        self._hand = hand

    @property
    def hand(self):
        return self._hand

    def name(self):
        return self._name

    def get_rect(self):
        return pygame.Rect(self._x, self._y, 20*len(self._hand) + 64, 114)

    def display_hand(self, display):
        for index, card in enumerate(self._hand):
            # print(card.get_position(), 'posit')
            card.display_card(display, card.get_position())

    def set_hand_positions(self):
        x = self._x
        y = self._y + 30
        for index, card in enumerate(self._hand):
            if index == len(self._hand) - 1:
                card.set_card_rect([x, y, 84, 114])
                card.set_position([x, y])
            else:
                card.set_position([x, y])
                card.set_card_rect([x, y, 20, 114])
            x += 20

    def display_player(self, display, font):
        text = font.render(self._name, False, (0, 0, 0))
        display.blit(text, (self._x, self._y))


class Stack:
    def __init__(self, position, stack_rules=None):
        self._active = False
        self._stack = []
        self._stack_rules = stack_rules
        self._size = [84, 114]
        self._position = position

    def get_position(self):
        return self._position

    def get_stack_rect(self):
        return pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])

    def display_stack(self, display):
        self._stack[len(self._stack) - 1].display_card(display, self._position)

    def remove_from_stack(self, card_to_remove, player):
        for index, card in enumerate(self._stack):
            if card_to_remove == card:
                del self._stack[index]

    def add_to_stack(self, card):
        if self.validate_move(card):
            self._stack.append(card)
        else:
            raise InvalidCardError()

    def top_card_from_stack(self, player):
        self._stack.remove(self._stack)

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
        if card.value in self._stack_rules['Values'][self.top_card().value]:
            return (self._stack_rules['Values'][self.top_card().value][card.value],
                    self._stack_rules['Values'][self.top_card().value]['Enforced'])
        else:
            return (self._stack_rules['Values'][self.top_card().value]['Default'],
                    self._stack_rules['Values'][self.top_card().value]['Enforced'])

    def validate_move(self, card):
        if self._stack_rules is None:
            return True
        elif self.top_card() is None:
            if card.suit in self._stack_rules['None']:
                # Further validation
                suit = self._stack_rules['None'][card.suit]
            else:
                return self._stack_rules['None']['Default']
        else:
            v_suit = self.validate_suit(card)
            v_value = self.validate_value(card)
            if v_suit[1] and v_value[1]:  # Both Enforced
                return v_suit[0] and v_value[0]
            elif v_suit[1] and not v_value[1]:  # Suit is Enforced
                return v_suit[0]
            elif not v_suit[1] and v_value[1]:  # Value is Enforced
                return v_value[0]
            elif not v_suit[1] and not v_value[1]:  # Nothing is enforced
                return v_value[0] or v_suit[0]


class Game:

    def __init__(self, players, stack, deck):
        self._stack = stack
        self._deck = deck
        self._players = players
        self._player_turn = players[0]
        self._screen = pygame.display.set_mode([800, 550])
        self._reversed = False
        self._actions = {}
        self._font = pygame.font.SysFont('Helvetica', 20)

    def generate(self):
        self._screen.fill((0, 128, 0))
        self._deck.display_deck(self._screen)
        # self._deck.display_top_card(self._screen)
        self._stack.display_stack(self._screen)
        for player in self._players:
            player.display_hand(self._screen)
            player.display_player(self._screen, self._font)
        pygame.display.flip()

    def reverse(self):
        self._reversed = not self._reversed
        self.set_next_player_turn()

    def set_player_turn(self, player):
        self._player_turn = player

    def set_next_player_turn(self):
        if self._reversed:
            currentTurn = self._players.index(self._player_turn)
            if currentTurn == 0:
                currentTurn = len(self._players) - 1
            else:
                currentTurn -= 1
        else:
            currentTurn = self._players.index(self._player_turn)
            if currentTurn == len(self._players) - 1:
                currentTurn = 0
            else:
                currentTurn += 1

        self._player_turn = self._players[currentTurn]

    @property
    def player_turn(self):
        return self._player_turn

    def set_card_action(self, card_name, action):
        self._actions[card_name] = action

    def set_value_action(self, card_name, action):
        self._actions[card_name] = action

    def set_suit_action(self, card_suit, action):
        self._actions[card_suit] = action

    def action(self, card):
        if card.card_name() in self._actions:
            self._actions[card.card_name()]()
        elif card.value in self._actions:
            self._actions[card.value]()
        elif card.suit in self._actions:
            self._actions[card.suit]()
        else:
            self.set_next_player_turn()

    def skip_turn(self):
        self.set_next_player_turn()
        self.set_next_player_turn()

    def move(self, player, card):
        if player == self._player_turn:
            player.play_card(card, self._stack)
            self.action(card)
        else:
            raise InvalidTurnError

    def pass_turn(self, player):
        if player == self._player_turn:
            self.set_next_player_turn()
        else:
            raise InvalidTurnError


class Deck:
    def __init__(self, location):
        self._deck = self.create()
        self._back_image = 'images/card-back.png'
        self._back_image = pygame.image.load(self._back_image)
        self._back_image = pygame.transform.scale(self._back_image, (84, 114))
        self._x = location[0]
        self._y = location[1]
        self._rect = pygame.Rect(location[0] + 90, location[1], 84, 114)

    def get_rect(self):
        return self._rect

    def get_position(self):
        return [self._x + 90, self._y]

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

    def draw_to_stack(self, stack):
        top_card = self._deck[len(self._deck) - 1]
        stack.add_to_stack(top_card)
        self.remove_card(top_card)

    def shuffle(self):
        random.shuffle(self._deck)

    def get_top_card(self):
        return self._deck[len(self._deck) - 1]

    def display_deck(self, display):
        display.blit(self._back_image, (self._x, self._y))

    def display_top_card(self, display):
        self.get_top_card().display_card(display, [self._x + 90, self._y])

    def deck(self):
        return self._deck
