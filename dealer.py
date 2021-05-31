class Dealer:
    def __init__(self, deck, players):
        self._deck = deck
        self._players = players

    def deal(self, card_count=52):
        # card_count takes amount of cards per player, then multiplies by number of players
        # Deals all cards if not provided
        cp_index = 0
        ttl_players = len(self._players)
        if card_count != 52:
            card_count = card_count * len(self._players)
        for card in self._deck.deck()[:card_count]:
            self._players[cp_index].add_to_hand(card)
            cp_index += 1
            self._deck.remove_card(card)
            if cp_index >= ttl_players:
                cp_index = 0

    def deal_to_player(self, player, cards):
        if cards > len(self._deck.deck()):  # if nothing left to deal, deal the rest of the pack
            cards = len(self._deck.deck())
        dealt_cards = self._deck.deck()[:cards]
        player.add_multiple_to_hand(dealt_cards)
        self._deck.remove_multiple_cards(dealt_cards)

    def shuffle_deck(self):
        self._deck.shuffle()