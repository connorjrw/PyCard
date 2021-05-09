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
movingcard = [None, False]
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for player in [player1, player2]:
                for card in player.hand:
                    if card.get_card_rect().collidepoint(pygame.mouse.get_pos()):
                        movingcard[0] = card
                        movingcard[1] = True
                        movingcard[0].set_previous_position(movingcard[0].get_position())

        if movingcard[1]:
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]
            movingcard[0].set_position([x, y])
            movingcard[0].set_card_rect([x, y, 84, 114])

        if event.type == pygame.MOUSEBUTTONUP and movingcard[1]:
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]
            if stack.get_stack_rect().colliderect(movingcard[0].get_card_rect()):
                # movingcard[0].set_position([])
                # movingcard[0].set_card_rect(stack.get_stack_rect())
                game.move(game.player_turn, movingcard[0])
                # game.player_turn.set_hand_positions()
                # stack.add_to_stack(movingcard[0])
            else:
                movingcard[0].set_position(movingcard[0].get_previous_position())
            movingcard[1] = False

    game.generate()

# Done! Time to quit.
pygame.quit()