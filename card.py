import pygame


class Card:
    def __init__(self, suit, value):
        self._suit = suit
        self._value = value
        self._rect = pygame.Rect(0, 0, 0, 0)
        self._image = 'images/Cards/' + suit + value + '.png'
        self._facedown = 'images/card-back.png'
        self._position = [-1, -1]
        self._previous_position = []
        self._is_moving = False
        self._size = [84, 114]
        self._is_facedown = False
        self._hello = 'asd'

    def set_moving(self, value):
        self._is_moving = value

    @property
    def size(self):
        return self._size

    @property
    def is_moving(self):
        return self._is_moving

    def set_previous_position(self, position):
        self._previous_position = position

    def get_previous_position(self):
        return self._previous_position

    def card_name(self):
        return self._value + ' of ' + self._suit

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position
        self.set_card_rect([position[0], position[1], self._size[0], self._size[1]])

    @property
    def suit(self):
        return self._suit

    @property
    def value(self):
        return self._value

    @property
    def is_facedown(self):
        return self._is_facedown

    @suit.setter
    def suit(self, suit):
        self._suit = suit

    @value.setter
    def value(self, value):
        self._value = value

    @is_facedown.setter
    def is_facedown(self, is_facedown):
        self._is_facedown = is_facedown

    def display_card(self, display, location):
        if self.is_facedown:
            card_img = pygame.image.load(self._facedown)
        else:
            card_img = pygame.image.load(self._image)
        card_img = pygame.transform.scale(card_img, (self._size[0], self._size[1]))
        display.blit(card_img, ([self._position[0], self._position[1]]))

    def display_card_facedown(self, display, location):
        card_img = pygame.image.load(self._facedown)
        card_img = pygame.transform.scale(card_img, (self._size[0], self._size[1]))
        display.blit(card_img, [location[0], location[1]])

    def set_card_rect(self, position):
        self._rect = pygame.Rect(position[0], position[1], self._size[0], self._size[1])

    def get_card_rect(self):
        return self._rect
