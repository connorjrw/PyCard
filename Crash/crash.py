import pygame
from game import *
from deck import *
from player import *
from dealer import *
from Crash import crash_rules
# import pygame


class Crash(Game):
    def __init__(self, players, stack, deck, dealer, screen_size):
        super().__init__(players, stack, deck, dealer, screen_size)

    def play_card(self, player, card):
        super(Crash, self).play_card(player, card)
        self.set_next_player_turn()

    def pick_up_stack(self):
        self._player_turn.add_multiple_to_hand(stack.stack)
        stack.remove_all_from_stack()
        self.set_next_player_turn()

screen_size = [1200, 750]

pygame.init()
deck = Deck()
rules = crash_rules.rules
stack = Stack([screen_size[0] / 2 - 42, screen_size[1] / 2 - 57], rules)

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
crash = Crash(players, stack, deck, dealer, screen_size)
crash.add_turn_option('Pick Up', crash.pick_up_stack)

# Setting Default rules

dealer.deal()
# deck.draw_to_stack(stack)

# Run until the user asks to quit

while Crash.running:
    for event in pygame.event.get():
        crash.handle_event(event)
    crash.generate()

pygame.quit()
