from errors import *
import pygame


class Player:
    def __init__(self, name):
        self._name = name
        self._hand = []
        self._location = [0, 0]
        self._player_name_loc = 'Above'
        self._option_loc = 0
        self._stacks = []

    @property
    def stacks(self):
        return self._stacks

    @stacks.setter
    def stacks(self, value):
        self._stacks = value

    @property
    def option_loc(self):
        return self._option_loc

    @option_loc.setter
    def option_loc(self, value):
        self._option_loc = value

    @property
    def player_name_loc(self):
        return self._player_name_loc

    @player_name_loc.setter
    def player_name_loc(self, location):
        self._player_name_loc = location

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, value):
        self._hand = value

    @property
    def name(self):
        return self._name

    def display_stacks(self, display):
        for stack in self._stacks:
            # print(type(stack.stack[0]))
            stack.display_stack(display)

    def add_to_hand(self, card):
        self._hand.append(card)
        self.set_hand_positions()

    def add_multiple_to_hand(self, cards):
        for card in cards:
            self._hand.append(card)
        self.set_hand_positions()

    def remove_from_hand(self, card):
        found = False
        if card in self._hand:
            self._hand.remove(card)
            self.set_hand_positions()
            found = True
        else:
            for stack in self._stacks:
                if card in stack.stack:
                    stack.remove_from_stack(card)
                    found = True
        if not found:
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
        # raise CardNotInHandError()

    def play_card(self, card, stack):
        stack.add_to_stack(card)
        self.remove_from_hand(card)

    def get_card(self, card_name):
        return self._hand[self.card_list_string().index(card_name)]

    def get_rect(self):
        return pygame.Rect(self._location[0], self._location[1], 20*len(self._hand) + 64, 114)

    def display_hand(self, display):
        for index, card in enumerate(self._hand):
            card.display_card(display, card.get_position())

    def display_hand_facedown(self, display):
        for index, card in enumerate(self._hand):
            card.display_card_facedown(display, card.get_position())

    def set_hand_positions(self):
        x = self._location[0] - (20 * (len(self._hand) / 2))
        y = self._location[1] + 30
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
        if self._player_name_loc == 'Below':
            display.blit(text, (self._location[0], self._location[1] + 150))
        else:
            display.blit(text, (self._location[0], self._location[1]))
