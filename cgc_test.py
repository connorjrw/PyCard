import unittest
from cg_create import *
from rules import  *


class AllTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AllTests, self).__init__(*args, **kwargs)

    def setUp(self):

        self.player1 = Player('Player1')
        self.player2 = Player('Player2')
        self.player3 = Player('Player3')
        self.players = [self.player1, self.player2, self.player3]
        self.newDeck = Deck()
        self.dealer = Dealer(self.newDeck, self.players)
        self.stack = Stack(rules)

    def test_deck(self):
        self.assertEqual(len(self.newDeck.deck), 52)
        self.assertEqual(self.newDeck.deck[0].card_name(), 'Ace of Diamonds')
        self.assertEqual(self.newDeck.deck[51].card_name(), 'King of Spades')
        
    def test_deal(self):
        self.dealer.deal()
        self.assertEqual(len(self.player1.hand), 18)
        self.assertEqual(len(self.player2.hand), 17)
        self.assertEqual(len(self.player2.hand), 17)
        self.assertEqual(len(self.newDeck.deck), 0)

    def test_deal_with_count(self):
        self.dealer.deal(7)
        self.assertEqual(len(self.player1.hand), 7)
        self.assertEqual(len(self.player2.hand), 7)
        self.assertEqual(len(self.player3.hand), 7)
        self.assertEqual(len(self.newDeck.deck), 31)

    def test_play_card(self):
        # self.dealer.shuffle_deck()
        self.dealer.deal()
        self.player1.playCard(self.player1.hand[0], self.stack)
        self.assertEqual(len(self.player1.hand), 17)
        self.assertEqual(len(self.stack.stack), 1)
        # self.player1.playCard(self.player1.hand[0], self.stack)
        # self.assertEqual(len(self.stack.stack), 2)

    def test_deal_num(self):
        self.dealer.deal_to_player(self.player1, 60)
        self.assertEqual(len(self.newDeck.deck), 0)
        self.assertEqual(len(self.player1.hand), 52)

    def test_next_player_turn(self):
        self.game = Game(self.players, self.stack)
        self.game.set_player_turn(self.player3)
        self.game.set_next_player_turn()
        self.assertEqual(self.game.player_turn.name(), self.player1.name())

    def test_get_card(self):
        self.dealer.deal()
        # self.assertEqual()

    def test_validation(self):
        newplayer = Player('new')
        newplayer.set_hand([Card('Spades', 'Ace'), Card('Spades', 'Three'), Card('Hearts', 'Three'), Card('Hearts', 'King')])
        newplayer.playCard(newplayer.hand[0], self.stack)
        newplayer.playCard(newplayer.hand[0], self.stack)
        newplayer.playCard(newplayer.hand[0], self.stack)
        newplayer.playCard(newplayer.hand[0], self.stack)

    def test_action(self):
        self.game = Game(self.players, self.stack)
        self.player1.set_hand([Card('Hearts', 'Ace'), Card('Spades', 'Three'), Card('Hearts', 'Three'), Card('Hearts', 'King')])
        self.player2.set_hand([Card('Hearts', 'Eight')])
        self.game.set_value_action('Eight', self.game.skip_turn)
        self.game.move(self.player1, self.player1.hand[0])
        self.game.move(self.player2, self.player2.hand[0])
        self.assertEqual(self.game.player_turn, self.player1)

    def test_reverse(self):
        self.game = Game(self.players, self.stack)
        self.game.set_value_action('Jack', self.game.reverse)
        self.player1.set_hand([Card('Diamonds', 'Seven'), Card('Diamonds', 'Ten')])
        self.player2.set_hand([Card('Diamonds', 'Jack')])
        self.game.move(self.player1, self.player1.hand[0])
        self.game.move(self.player2, self.player2.hand[0])
        self.assertEqual(self.game.player_turn, self.player1)
        self.game.move(self.player1, self.player1.hand[0])
        self.assertEqual(self.game.player_turn, self.player3)


if __name__ == '__main__':
    unittest.main()
