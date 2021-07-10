import pygame
import random
from card import Card


class Deck:
    def __init__(self, location=None):
        self._deck = self.create()
        self._back_image = 'images/card-back.png'
        self._back_image = pygame.image.load(self._back_image)
        self._back_image = pygame.transform.scale(self._back_image, (84, 114))
        self._x = None
        self._y = None
        self._rect = None
        if location is not None:
            self._x = location[0]
            self._y = location[1]
            self._rect = pygame.Rect(location[0] + 90, location[1], 84, 114)

    @property
    def rect(self):
        return self._rect  # Not sure if this used

    @property
    def deck(self):
        return self._deck

    # def get_position(self):
    #     return [self._x + 90, self._y] # think this can be removed
    @deck.setter
    def deck(self, value):
        self._deck = value

    def top_card(self):
        return self._deck[len(self._deck) - 1]

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

    def display_deck(self, display):
        if len(self._deck) > 0 and self._rect is not None: # Show nothing if deck is empty,
            display.blit(self._back_image, (self._x, self._y))

    def display_top_card(self, display):
        self.top_card().display_card(display, [self._x + 90, self._y])