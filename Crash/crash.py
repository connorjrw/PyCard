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



pygame.init()
deck = Deck()
rules = crash_rules.rules
stack = Stack([416, 186], rules)

deck.shuffle()

# Players
player1 = Player('Player 1')
player2 = Player('Player 2')
players = [player1, player2]

# dealer
dealer = Dealer(deck, players)

# font
pygame.font.init()

screen_size = [1000, 600]

# game init
crash = Crash(players, stack, deck, dealer, screen_size)

# Setting Default rules

dealer.deal()
# deck.draw_to_stack(stack)

# Run until the user asks to quit

while Crash.running:
    for event in pygame.event.get():
        crash.handle_event(event)
    crash.generate()

pygame.quit()
