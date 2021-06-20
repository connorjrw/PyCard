from errors import *
import pygame


class Player:
    def __init__(self, name):
        self._name = name
        self._hand = []
        self._x = 0
        self._y = 0

    def set_location(self, location):
        self._x = location[0]
        self._y = location[1]

    def get_location(self):
        return [self._x, self._y]

    def add_to_hand(self, card):
        self._hand.append(card)
        self.set_hand_positions()

    def add_multiple_to_hand(self, cards):
        for card in cards:
            self._hand.append(card)
        self.set_hand_positions()

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

    @property
    def name(self):
        return self._name

    def get_rect(self):
        return pygame.Rect(self._x, self._y, 20*len(self._hand) + 64, 114)

    def display_hand(self, display):
        for index, card in enumerate(self._hand):
            card.display_card(display, card.get_position())

    def display_hand_facedown(self, display):
        for index, card in enumerate(self._hand):
            card.display_card_facedown(display, card.get_position())

    def set_hand_positions(self):
        x = self._x - (20 * (len(self._hand) / 2))
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