import pygame
from last_card import lc_rules
from game import *
from deck import *
from player import *
from dealer import *
from copy import deepcopy


class LastCard(Game):
    def __init__(self, players, stack, deck, dealer):
        self._pickup_count = 0
        super().__init__(players, stack, deck, dealer)

    # todo: condense into one
    def draw_two_action(self):
        self._dealer.deal_to_player(self._player_turn, self._pickup_count)
        self.remove_all_turn_options()
        self.add_turn_option('Draw', self.deal_and_next_turn)
        self.set_next_player_turn()
        self._pickup_count = 0
        stack.update_rule({"Values": {"Two": {'Default': False, 'Two': True, 'Enforced': False}}})

    def draw_two(self):
        self.set_next_player_turn()
        self.remove_turn_option('Draw')
        self.add_turn_option('Draw ' + str(self._pickup_count), self.draw_two_action)

    def draw_five(self):
        self.set_next_player_turn()
        self.remove_turn_option('Draw')
        self.add_turn_option('Draw ' + str(self._pickup_count), self.draw_five_action)

    def draw_five_action(self):
        self._dealer.deal_to_player(self._player_turn, self._pickup_count)
        self.remove_all_turn_options()
        self.add_turn_option('Draw', self.deal_and_next_turn)
        self.set_next_player_turn()
        self._pickup_count = 0
        stack.update_rule({"Values": {"Five": {'Default': False, 'Five': True, 'Enforced': False}}})

    def play_card(self, player, card):
        super(LastCard, self).play_card(player, card)
        self.set_default_rules()
        self.allow_multiple_cards()
        self.remove_all_turn_options()
        if card.value == 'Two':
            self._pickup_count += 2
        if card.value == 'Five':
            self._pickup_count += 5
        # self.remove_turn_option('Draw')
        self.add_turn_option('Finish', lc.action)
        self.end_game_condition()

    def action(self):
        # stack.update_rules(lc_rules.rules)
        self.set_default_rules()
        self.remove_turn_option('Finish')
        self.add_turn_option('Draw', self.deal_and_next_turn)
        super(LastCard, self).action()

    def set_default_rules(self):
        ms_rules = deepcopy(lc_rules.rules)
        stack.update_rules(ms_rules)

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

    def choose_suit(self):
        self.remove_all_turn_options()
        self.add_turn_option('Diamonds', self.enforce_diamonds)
        self.add_turn_option('Clubs', self.enforce_clubs)
        self.add_turn_option('Spades', self.enforce_spades)
        self.add_turn_option('Hearts', self.enforce_hearts)

    def enforce_diamonds(self):
        self.enforce_suit('Diamonds')

    def enforce_clubs(self):
        self.enforce_suit('Clubs')

    def enforce_spades(self):
        self.enforce_suit('Spades')

    def enforce_hearts(self):
        self.enforce_suit('Hearts')

    def enforce_suit(self, e_suit):
        self.remove_all_turn_options()
        self.add_turn_option('Draw', self.deal_and_next_turn)
        self.set_next_player_turn()
        rules = self._stack.get_rules()
        values = rules['Values']
        suits = rules['Suits']
        for value in values:
            values[value]['Enforced'] = False
            values[value]['Default'] = True
        for suit in suits:
            suits[suit]['Enforced'] = True
            suits[suit]['Default'] = False
            suits[suit][suit] = False
            suits[suit][e_suit] = True
        rules = {"Values": values, "Suits": suits}
        stack.update_rule(rules)

pygame.init()
master_rules = deepcopy(lc_rules.rules)
deck = Deck([300, 193])
stack = Stack([390, 193], master_rules)

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
lc.set_value_action('Ace', lc.choose_suit)
lc.add_turn_option('Draw', lc.deal_and_next_turn)

# Setting Default rules
stack.update_rule({"Values": {"Two": {'Default': False, 'Two': True, 'Enforced': False}}})
stack.update_rule({"Values": {"Five": {'Default': False, 'Five': True, 'Enforced': False}}})

dealer.deal(2)
deck.draw_to_stack(stack)

# Run until the user asks to quit

while lc.running:
    for event in pygame.event.get():
        lc.handle_event(event)
    lc.generate()

pygame.quit()
