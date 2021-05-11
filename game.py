import pygame
from cardlogic import *
pygame.init()
deck = Deck([300, 193])
stack = Stack([390, 193])
deck.shuffle()
player1 = Player('connor', [10, 10])
player2 = Player('Minh', [490, 370])
dealer = Dealer(deck, [player1, player2])
dealer.deal(10)

pygame.font.init()
myfont = pygame.font.SysFont('Helvetica', 20)
# Set up the drawing window
screen = pygame.display.set_mode([800, 550])
deck_image = pygame.image.load(r'images/card-back.png')
deck_image = pygame.transform.scale(deck_image, (84, 114))

deck.draw_to_stack(stack)
game = Game([player1, player2], stack, deck)


# Run until the user asks to quit
running = True
current_card = None
is_moving = False

x_buf = 0
y_buf = 0
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for player in [player1, player2]:
                for card in player.hand:
                    if card.get_card_rect().collidepoint(pygame.mouse.get_pos()) and game.player_turn == player:
                        current_card = card
                        is_moving = True
                        current_card.set_previous_position(current_card.get_position())

                        # Get difference between cursor and top of card
                        x_buf = pygame.mouse.get_pos()[0] - current_card.get_position()[0]
                        y_buf = pygame.mouse.get_pos()[1] - current_card.get_position()[1]

        if is_moving:
            # Card follows cursor while moving

            x = pygame.mouse.get_pos()[0] - x_buf
            y = pygame.mouse.get_pos()[1] - y_buf

            current_card.set_position([x, y])
            current_card.set_card_rect([x + x_buf, y + y_buf, 84, 114])

        if event.type == pygame.MOUSEBUTTONUP and is_moving:
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]
            if stack.get_stack_rect().colliderect(current_card.get_card_rect()):
                game.move(game.player_turn, current_card)
            else:
                current_card.set_position(current_card.get_previous_position())
            is_moving = False

    game.generate()

# Done! Time to quit.
pygame.quit()