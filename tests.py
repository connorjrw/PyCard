import unittest
from cardlogic import *
from rules import *
from errors import *


class TestDeal(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDeal, self).__init__(*args, **kwargs)

    def setUp(self):
        self.test_player_one = Player('P1')
        self.test_player_two = Player('P2')
        self.test_player_three = Player('P3')
        self.players = [self.test_player_one, self.test_player_two, self.test_player_three]
        self.test_deck = Deck()
        self.dealer = Dealer(self.test_deck, self.players)

    def verify_deck(self):
        self.assertEqual(len(self.test_deck.deck), 52)
        self.assertEqual(self.test_deck.deck[0].card_name(), 'Ace of Diamonds')
        self.assertEqual(self.test_deck.deck[51].card_name(), 'King of Spades')
        # check for duplicates, check all cards are in?

    def test_deal_all(self):
        self.dealer.deal()
        self.assertEqual(len(self.test_player_one.hand), 18)
        self.assertEqual(len(self.test_player_two.hand), 17)
        self.assertEqual(len(self.test_player_three.hand), 17)
        self.assertEqual(len(self.test_deck.deck), 0)

    def test_deal_seven(self):
        # Seven to each player
        self.dealer.deal(7)
        self.assertEqual(len(self.test_player_one.hand), 7)
        self.assertEqual(len(self.test_player_two.hand), 7)
        self.assertEqual(len(self.test_player_three.hand), 7)
        self.assertEqual(len(self.test_deck.deck), 31)

    def test_deal_max(self):
        # Should we get an error?
        self.dealer.deal(20)
        self.assertEqual(len(self.test_player_one.hand), 18)


class TestGame(unittest.TestCase):
    def setUp(self):
        self.test_player_one = Player('P1')
        self.test_player_two = Player('P2')
        self.deck = Deck()
        self.players = [self.test_player_one, self.test_player_two]
        self.dealer = Dealer(self.deck, self.players)
        self.game = Game(self.players, Stack())
        self.dealer.deal()

    def test_turn(self):
        self.game.move(self.test_player_one, self.test_player_one.hand[0])
        with self.assertRaises(InvalidTurnError):
            self.game.move(self.test_player_one, self.test_player_one.hand[0])

    def test_play_card(self):
        with self.assertRaises(CardNotInHandError):
            self.game.move(self.test_player_one, self.test_player_two.hand[0])


class TestActions(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestActions, self).__init__(*args, **kwargs)

    def setUp(self):
        self.test_player_one = Player('P1')
        self.test_player_two = Player('P2')
        self.test_player_three = Player('P3')
        self.test_player_one.set_hand([Card('Clubs', 'Ace'), Card('Clubs', 'Four')])
        self.test_player_two.set_hand([Card('Clubs', 'Two')])
        self.test_player_three.set_hand([Card('Clubs', 'Two')])
        self.players = [self.test_player_one, self.test_player_two, self.test_player_three]
        self.game = Game(self.players, Stack())

    def test_skip_turn(self):
        self.game.set_value_action('Ace', self.game.skip_turn)
        self.game.move(self.test_player_one, self.test_player_one.hand[0])
        self.assertEqual(self.game.player_turn, self.test_player_three)

    def test_reverse(self):
        self.game.set_value_action('Two', self.game.reverse)
        self.game.move(self.test_player_one, self.test_player_one.hand[0])
        self.game.move(self.test_player_two, self.test_player_two.hand[0])
        self.assertEqual(self.game.player_turn, self.test_player_one)
        self.game.move(self.test_player_one, self.test_player_one.hand[0])
        self.assertEqual(self.game.player_turn, self.test_player_three)
        self.game.move(self.test_player_three, self.test_player_three.hand[0]) # Reverse back to original
        self.assertEqual(self.game.player_turn, self.test_player_one)


class TestRules(unittest.TestCase):
    def setUp(self):
        self.test_player_one = Player('P1')
        self.test_player_two = Player('P2')
        self.test_player_three = Player('P3')
        self.test_player_one.set_hand([Card('Clubs', 'King'), Card('Clubs', 'Ace')])
        self.test_player_two.set_hand([Card('Clubs', 'Queen'), Card('Hearts', 'Ace')])
        self.test_player_three.set_hand([Card('Hearts', 'Three')])
        self.players = [self.test_player_one, self.test_player_two, self.test_player_three]
        self.game = Game(self.players, Stack(rules))

    def test_suit(self):
        self.game.move(self.test_player_one, self.test_player_one.hand[0])
        self.game.move(self.test_player_two, self.test_player_two.hand[0])
        with self.assertRaises(InvalidCardError):
            self.game.move(self.test_player_three, self.test_player_three.hand[0])
        self.assertEqual(self.game.player_turn, self.test_player_three)  # Check that it's still p3's turn

    def test_enforced(self):
        self.game.move(self.test_player_one, self.test_player_one.hand[1])
        with self.assertRaises(InvalidCardError):
            self.game.move(self.test_player_two, self.test_player_two.hand[0])
        self.game.move(self.test_player_two, self.test_player_two.hand[1])


if __name__ == '__main__':
    unittest.main()
