import pygame
from errors import *


class Stack:
    def __init__(self, position, stack_rules=None):
        self._active = False
        self._stack = []
        self._stack_rules = stack_rules
        self._size = [84, 114]
        self._position = position

    def update_rules(self, rules):
        print('updating rules')
        self._stack_rules = rules

    def update_rule(self, update):
        if "Suits" in update:
            for suit in self._stack_rules['Suits']:
                if suit in update["Suits"]:
                    self._stack_rules['Suits'][suit] = update["Suits"][suit]
        if "Values" in update:
            for value in self._stack_rules['Values']:
                if value in update["Values"]:
                    self._stack_rules['Values'][value] = update["Values"][value]

    def get_rules(self):
        return self._stack_rules

    def get_position(self):
        return self._position

    def set_stack(self, stack):
        self._stack = stack

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
            return (self._stack_rules['Suits'][self.top_card().suit]['Default'],
                    self._stack_rules['Suits'][self.top_card().suit]['Enforced'])

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
            print('values', v_suit, v_value)
            if v_suit[1] and v_value[1]:  # Both Enforced
                return v_suit[0] and v_value[0]
            elif v_suit[1] and not v_value[1]:  # Suit is Enforced
                return v_suit[0]
            elif not v_suit[1] and v_value[1]:  # Value is Enforced
                return v_value[0]
            elif not v_suit[1] and not v_value[1]:  # Nothing is enforced
                return v_value[0] or v_suit[0]