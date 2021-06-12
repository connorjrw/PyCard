import pygame
from last_card import lc_rules
from game import *
from deck import *
from player import *
from dealer import *


class LastCard(Game):
    def __init__(self, players, stack, deck, dealer):
        self._pickup_count = 0
        super().__init__(players, stack, deck, dealer)

    # todo: condense into one
    def draw_two_action(self):
        self._dealer.deal_to_player(self._player_turn, self._pickup_count)
        self.remove_turn_option('Draw Two')
        self.add_turn_option('Draw', self.deal_and_next_turn)
        self.set_next_player_turn()
        self._pickup_count = 0
        stack.update_rule({"Values": {"Two": {'Default': False, 'Two': True, 'Enforced': False}}})

    def draw_two(self):
        self._pickup_count += 2
        self.set_next_player_turn()
        self.remove_turn_option('Draw')
        self.add_turn_option('Draw Two', self.draw_two_action)

    def draw_five(self):
        self.set_next_player_turn()
        self.remove_turn_option('Draw')
        self.add_turn_option('Draw Five', self.draw_five_action)

    def draw_five_action(self):
        self._dealer.deal_to_player(self._player_turn, 5)
        self.remove_turn_option('Draw Five')
        self.add_turn_option('Draw', self.deal_and_next_turn)
        self.set_next_player_turn()
        self._pickup_count = 0
        stack.update_rule({"Values": {"Five": {'Default': False, 'Five': True, 'Enforced': False}}})

    def play_card(self, player, card):
        super(LastCard, self).play_card(player, card)
        self.allow_multiple_cards()
        self.remove_turn_option('Draw')
        self.add_turn_option('Finish', lc.action)

    def action(self):
        # stack.update_rules(lc_rules.rules)
        self.set_default_rules()
        self.remove_turn_option('Finish')
        self.add_turn_option('Draw', self.deal_and_next_turn)
        super(LastCard, self).action()

    def set_default_rules(self):
        rules = self._stack.get_rules()
        values = rules['Values']
        suits = rules['Suits']
        for value in values:
            values[value]['Enforced'] = False
            if values[value][value]:
                values[value][value] = True
            if value == 'Two' or value == 'Five':
                values[value]['Enforced'] = True
        for suit in suits:
            suits[suit]['Enforced'] = False
        rules = {"Values": values, "Suits": suits}
        stack.update_rule(rules)

    def allow_multiple_cards(self):
        rules = self._stack.get_rules()
        values = rules['Values']
        suits = rules['Suits']
        for value in values:
            values[value]['Enforced'] = True
        for suit in suits:
            suits[suit]['Enforced'] = False
        rules = {"Values": values, "Suits": suits}
        stack.update_rule(rules)


pygame.init()

deck = Deck([300, 193])
stack = Stack([390, 193], lc_rules.rules)

deck.shuffle()

# Players
player1 = Player('Player 1')
player2 = Player('Player 2')
player3 = Player('Player 3')
player4 = Player('Player 4')
players = [player1, player2, player3, player4]

# dealer
dealer = Dealer(deck, players)

# font
pygame.font.init()

# Set up the drawing window
screen = pygame.display.set_mode([800, 550])

# game init
lc = LastCard(players, stack, deck, dealer)
lc.set_value_action('Eight', lc.skip_turn)
lc.set_value_action('Jack', lc.reverse)
lc.set_value_action('Two', lc.draw_two)
lc.set_value_action('Five', lc.draw_five)
lc.add_turn_option('Draw', lc.deal_and_next_turn)

# Setting Default rules
stack.update_rule({"Values": {"Two": {'Default': False, 'Two': True, 'Enforced': False}}})
stack.update_rule({"Values": {"Five": {'Default': False, 'Five': True, 'Enforced': False}}})

dealer.deal(12)
deck.draw_to_stack(stack)

# Run until the user asks to quit
running = True

while running:
    for event in pygame.event.get():
        lc.handle_event(event)
    lc.generate()
pygame.quit()
