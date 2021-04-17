import unittest
from main import *


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
        self.newDeck.create()
        self.stack = Stack()

    def test_deck(self):
        self.assertEqual(len(self.newDeck.deck), 52)
        self.assertEqual(self.newDeck.deck[0].cardAsString(), 'Ace of Diamonds')
        self.assertEqual(self.newDeck.deck[51].cardAsString(), 'King of Spades')
        
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
        self.dealer.deal()
        self.player1.playCard(self.player1.hand[0], self.stack)
        self.assertEqual(len(self.player1.hand), 17)
        self.assertEqual(len(self.stack.stack), 1)

    def test_deal_num(self):
        self.dealer.dealToPlayer(self.player1, 60)
        self.assertEqual(len(self.newDeck.deck), 0)
        self.assertEqual(len(self.player1.hand), 52)

    def test_next_player_turn(self):
        self.game = Game(self.players)
        self.game.setPlayerTurn(self.player3)
        self.game.setNextPlayerTurn()
        self.assertEqual(self.game.playerTurn.name(), self.player1.name())


if __name__ == '__main__':
    unittest.main()
