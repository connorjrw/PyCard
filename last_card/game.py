import pygame
from last_card import lc_rules
from cardlogic import *


pygame.init()

deck = Deck([300, 193])
stack = Stack([390, 193], lc_rules.rules)


deck.shuffle()
print(pygame.font.get_fonts())
# Players
player1 = Player('Connor')
player2 = Player('Minh')
player3 = Player('Mori')
player4 = Player('Moto')
players = [player1, player2, player3, player4]

# dealer
dealer = Dealer(deck, players)

#font
pygame.font.init()
myfont = pygame.font.SysFont('Helvetica', 20)


# Set up the drawing window
screen = pygame.display.set_mode([800, 550])


# game init
game = Game(players, stack, deck, dealer)
game.set_value_action('Eight', game.skip_turn)
game.set_value_action('Jack', game.reverse)
game.set_value_action('Two', game.draw_two)
# game.add_turn_option('Done', game.set_next_player_turn)
game.add_turn_option('Draw', game.deal_and_next_turn)


dealer.deal(10)
deck.draw_to_stack(stack)


# Run until the user asks to quit
running = True
current_card = None
is_moving = False

x_buf = 0
y_buf = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for player in players:
                for card in player.hand:
                    if card.get_card_rect().collidepoint(pygame.mouse.get_pos()) and game.player_turn == player:
                        current_card = card
                        is_moving = True
                        current_card.set_previous_position(current_card.get_position())

                        # Get difference between cursor and top of card
                        x_buf = pygame.mouse.get_pos()[0] - current_card.get_position()[0]
                        y_buf = pygame.mouse.get_pos()[1] - current_card.get_position()[1]
            for button in game.turn_options:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.action()
        if is_moving:
            # Drag card

            x = pygame.mouse.get_pos()[0] - x_buf
            y = pygame.mouse.get_pos()[1] - y_buf

            current_card.set_position([x, y])
            current_card.set_card_rect([x + x_buf, y + y_buf, 84, 114])

        if event.type == pygame.MOUSEBUTTONUP and is_moving:
            # Stop dragging card
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]
            if stack.get_stack_rect().colliderect(current_card.get_card_rect()):
                try:
                    game.move(game.player_turn, current_card)
                except InvalidCardError:
                    # Also error
                    current_card.set_position(current_card.get_previous_position())
            else:
                current_card.set_position(current_card.get_previous_position())
            is_moving = False

    game.generate()

pygame.quit()
