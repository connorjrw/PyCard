import pygame


class TurnOptionButton:
    def __init__(self, name, action):
        self._name = name
        self._action = action
        self._x = 0
        self._y = 0
        self._rect = pygame.Rect(0, 0, 0, 0)

    def set_rect(self, dimen):
        self._rect = pygame.Rect(dimen[0], dimen[1], dimen[2], dimen[3])

    @property
    def name(self):
        return self._name

    @property
    def rect(self):
        return self._rect

    @property
    def action(self):
        return self._action