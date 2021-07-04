import pygame
from game import *
from deck import *
from player import *
from dealer import *
from Crash import crash_rules
from copy import deepcopy
# import pygame


class Crash(Game):
    def __init__(self, players, stacks, deck, dealer, screen_size, player_turn_iden):
        super().__init__(players, stacks, deck, dealer, screen_size, player_turn_iden)

    def play_card(self, player, card):
        super(Crash, self).play_card(player, card)
        card.is_facedown = False
        self.allow_multiple_cards()
        self.add_turn_option('Finish', self.action)

    def action(self):
        super(Crash, self).action()
        self.set_default_rules()
        self.remove_turn_option('Finish')

    def play_and_pick_up(self):
        self._player_turn.remove_from_hand(self._current_card)
        self.pick_up_stack()

    def pick_up_stack(self):
        self._player_turn.add_multiple_to_hand(self.current_stack.stack)
        self.current_stack.remove_all_from_stack()
        self.set_next_player_turn()

    def add_to_generate(self):
        self.validate_stack_status()

    def allow_all_cards(self):
        rules = deepcopy(self._stacks[0].get_rules())
        for value in rules['Values']:
            rules['Values'][value]['Rank'] = 0
        stacks[0].update_rules(rules)

    def set_default_rules(self):
        ms_rules = deepcopy(crash_rules.rules)
        stacks[0].update_rule(ms_rules)

    def allow_multiple_cards(self):
        current_rules = deepcopy(crash_rules.rules)
        values = current_rules['Values']
        suits = current_rules['Suits']
        for value in values:
            values[value][value] = True
            values[value]['Rank'] = None
            values[value]['Enforced'] = True
        for suit in suits:
            suits[suit]['Enforced'] = False
        new_rules = {"Values": values, "Suits": suits}
        self._stacks[0].update_rule(new_rules)

    def validate_stack_status(self):
        self._stacks[0].set_rule_action(None)
        left = self.player_turn.stacks[0]
        mid = self.player_turn.stacks[1]
        right = self.player_turn.stacks[2]
        # self.set_default_rules()
        if len(self.player_turn.hand) == 0:
            left.locked = False
            mid.locked = False
            right.locked = False
        if len(self.player_turn.hand) > 0:
            left.locked = True
            mid.locked = True
            right.locked = True
        else:
            if len(left.stack) == 1:
                left.locked = True
            if len(mid.stack) == 1:
                mid.locked = True
            if len(right.stack) == 1:
                right.locked = True
            if len(left.stack) <= 1 and len(mid.stack) <= 1 and len(right.stack) <= 1:
                # self.allow_all_cards()
                self._stacks[0].set_rule_action(self.play_and_pick_up)
                left.locked = False
                mid.locked = False
                right.locked = False

    def create_stacks(self):
        for player in self._players:
            y = deepcopy(player.get_location()[1])
            x = screen_size[0] / 2 - 136
            player_stacks = []
            if player.player_name_loc == 'Above':
                y += 150
            else:
                y -= 100
            for i in range(3):
                current_stack = Stack([x, y])
                dealer.deal_to_stack(current_stack, 2)
                current_stack.stack[0].is_facedown = True
                player_stacks.append(current_stack)
                x += 100
            player.set_stacks(player_stacks)

    def clear_pile(self):
        self._stacks[0].stack = []

screen_size = [1200, 750]

pygame.init()
deck = Deck()
rules = deepcopy(crash_rules.rules)
stacks = [Stack([screen_size[0] / 2 - 42, screen_size[1] / 2 - 57], rules)]
player_turn_iden = stacks[0].get_position()[0], stacks[0].get_position()[1] + 120 # Add as paramater


deck.shuffle()

# Players
player1 = Player('Player 1')
player2 = Player('Player 2')
players = [player1, player2]

# dealer
dealer = Dealer(deck, players)


# font
pygame.font.init()



# game init
crash = Crash(players, stacks, deck, dealer, screen_size, player_turn_iden)
crash.create_stacks()
crash.add_turn_option('Pick Up', crash.pick_up_stack)
crash.set_value_action('Ten', crash.clear_pile)
crash.set_sequence_action(4, crash.clear_pile)

# Setting Default rules

dealer.deal(5)
crash.validate_stack_status()

# deck.draw_to_stack(stack)

# Run until the user asks to quit

while Crash.running:
    for event in pygame.event.get():
        crash.handle_event(event)
    crash.generate()

pygame.quit()
