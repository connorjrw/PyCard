import pygame
from last_card import lc_rules, lc_rules2
from cardlogic import *


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
        stack.update_rules(lc_rules2.rules)
        self.remove_turn_option('Draw')
        self.add_turn_option('Finish', lc.action)

    def action(self):
        stack.update_rules(lc_rules.rules)
        self.remove_turn_option('Finish')
        self.add_turn_option('Draw', self.deal_and_next_turn)
        super(LastCard, self).action()


pygame.init()

deck = Deck([300, 193])
stack = Stack([390, 193], lc_rules.rules)


deck.shuffle()

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
lc = LastCard(players, stack, deck, dealer)
lc.set_value_action('Eight', lc.skip_turn)
lc.set_value_action('Jack', lc.reverse)
lc.set_value_action('Two', lc.draw_two)
lc.set_value_action('Five', lc.draw_five)
lc.add_turn_option('Draw', lc.deal_and_next_turn)


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
                    if card.get_card_rect().collidepoint(pygame.mouse.get_pos()) and lc.player_turn == player:
                        current_card = card
                        is_moving = True
                        current_card.set_previous_position(current_card.get_position())

                        # Get difference between cursor and top of card
                        x_buf = pygame.mouse.get_pos()[0] - current_card.get_position()[0]
                        y_buf = pygame.mouse.get_pos()[1] - current_card.get_position()[1]
            for button in lc.turn_options:
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
                    lc.play_card(lc.player_turn, current_card)
                except InvalidCardError:
                    # Also error
                    current_card.set_position(current_card.get_previous_position())
            else:
                current_card.set_position(current_card.get_previous_position())
            is_moving = False

    lc.generate()

pygame.quit()
