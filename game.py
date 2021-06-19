from button import *
from stack import *


class Game:

    def __init__(self, players, stack, deck, dealer):
        self._stack = stack
        self._deck = deck
        self._players = players
        self._player_turn = players[0]
        self._dealer = dealer
        self._turn_options = []
        self._current_card = None
        self._x_buf = 0
        self._y_buf = 0
        self.set_player_location()
        self._screen = pygame.display.set_mode([800, 550])
        self._reversed = False
        self._actions = {}
        self._font = pygame.font.SysFont('timesnewromanbold', 20)
        self._player_turn_iden = [305, 315] # Add as paramater
        self._running = True

    @property
    def running(self):
        return self._running

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('asd')
            for player in self._players:
                for card in player.hand:
                    if card.get_card_rect().collidepoint(pygame.mouse.get_pos()) and self._player_turn == player:
                        self._current_card = card
                        self._current_card.set_moving(True)
                        self._current_card.set_previous_position(self._current_card.get_position())

                        # Get difference between cursor and top of card
                        self._x_buf = pygame.mouse.get_pos()[0] - self._current_card.get_position()[0]
                        self._y_buf = pygame.mouse.get_pos()[1] - self._current_card.get_position()[1]
            for button in self._turn_options:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.action()

        if self._current_card:
            if self._current_card.is_moving:
                # Drag card
                x = pygame.mouse.get_pos()[0] - self._x_buf
                y = pygame.mouse.get_pos()[1] - self._y_buf

                self._current_card.set_position([x, y])
                self._current_card.set_card_rect([x + self._x_buf, y + self._y_buf, 84, 114])

            if event.type == pygame.MOUSEBUTTONUP and self._current_card.is_moving:
            # Stop dragging card
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if self._stack.get_stack_rect().colliderect(self._current_card.get_card_rect()):
                    try:
                        self.play_card(self._player_turn, self._current_card)
                    except InvalidCardError:
                        # Also error
                        self._current_card.set_position(self._current_card.get_previous_position())
                else:
                    self._current_card.set_position(self._current_card.get_previous_position())
                self._current_card.set_moving(False)

    @property
    def turn_options(self):
        return self._turn_options

    def remove_turn_option(self, name):
        for turn in self._turn_options:
            if turn.name == name:
                self._turn_options.remove(turn)

    def remove_all_turn_options(self):
        self._turn_options = []

    def add_turn_option(self, name, action):
        exists = False
        for turn_option in self._turn_options:
            print(turn_option.name, name)
            if turn_option.name == name:
                exists = True
        if not exists:
            self._turn_options.append(TurnOptionButton(name, action))

    def show_turn_options(self, display, font):
        font = pygame.font.SysFont('timesnewromanbold', 16)
        color = (220, 220, 220)
        loc = self._player_turn.get_location()
        x = loc[0]
        y = loc[1] + 150
        for turn in self._turn_options:
            turn.set_rect(pygame.Rect(x, y, 70, 25))
            pygame.draw.rect(display, color, pygame.Rect(x, y, 70, 25))
            text = font.render(turn.name, False, (0, 0, 0))
            display.blit(text, (x + 10, y))
            x += 75

    def set_player_location(self):
        if len(self._players) == 1:
            self._players[0].set_location([10,10])
        elif len(self._players) == 2:
            self._players[0].set_location([10, 10])
            self._players[1].set_location([490, 370])
        elif len(self._players) == 3:
            self._players[0].set_location([10, 10])
            self._players[1].set_location([490, 370])
            self._players[2].set_location([10, 370])
        elif len(self._players) == 4:
            self._players[0].set_location([10, 10])
            self._players[1].set_location([490, 10])
            self._players[2].set_location([490, 370])
            self._players[3].set_location([10, 370])

    def generate(self):
        # If the deck is empty, move all but top card from stack back to deck
        if len(self._deck.deck()) == 0 and len(self._stack.stack) > 1:
            self._deck.set_deck(self._stack.stack[:-1])
            self._stack.set_stack([self._stack.stack[len(self._stack.stack) - 1]])
            self._deck.shuffle()
        self._screen.fill((0, 128, 0))
        self._deck.display_deck(self._screen)
        self.show_player_turn(self._screen, self._font)
        self.show_turn_options(self._screen, self._font)
        # self._deck.display_top_card(self._screen)
        self._stack.display_stack(self._screen)
        for player in self._players:
            player.display_hand(self._screen)
            player.display_player(self._screen, self._font)

            # if player == self._player_turn:
            #     player.display_hand(self._screen)
            # else:  # Hide cards if not the players turn
            #     player.display_hand_facedown(self._screen)
        pygame.display.flip()

    def reverse(self):
        self._reversed = not self._reversed
        self.set_next_player_turn()

    def set_player_turn(self, player):
        self._player_turn = player

    def set_next_player_turn(self):
        if self._reversed:
            currentTurn = self._players.index(self._player_turn)
            if currentTurn == 0:
                currentTurn = len(self._players) - 1
            else:
                currentTurn -= 1
        else:
            currentTurn = self._players.index(self._player_turn)
            if currentTurn == len(self._players) - 1:
                currentTurn = 0
            else:
                currentTurn += 1

        self._player_turn = self._players[currentTurn]

    @property
    def player_turn(self):
        return self._player_turn

    def set_card_action(self, card_name, action):
        self._actions[card_name] = action

    def set_value_action(self, card_name, action):
        self._actions[card_name] = action

    def set_suit_action(self, card_suit, action):
        self._actions[card_suit] = action

    def action(self):
        card = self._stack.top_card()
        if card.card_name() in self._actions:
            self._actions[card.card_name()]()
        elif card.value in self._actions:
            self._actions[card.value]()
        elif card.suit in self._actions:
            self._actions[card.suit]()
        else:
            self.set_next_player_turn()

    def skip_turn(self):
        self.set_next_player_turn()
        self.set_next_player_turn()

    def play_card(self, player, card):
        if player == self._player_turn:
            player.play_card(card, self._stack)
            # self.action()
        else:
            raise InvalidTurnError

    def show_player_turn(self, display, font):
        text = font.render(self._player_turn.name + "'s turn", False, (0, 0, 0))
        display.blit(text, (self._player_turn_iden[0], self._player_turn_iden[1]))

    def pass_turn(self, player):
        if player == self._player_turn:
            self.set_next_player_turn()
        else:
            raise InvalidTurnError

    def deal_and_next_turn(self):
        self._dealer.deal_to_player(self._player_turn, 1)
        self.set_next_player_turn()

    def end_game_condition(self):
        for player in self._players:
            if len(player.hand) == 0:
                self._running = False
                print(self._running, 'Running')
