from cg_create import *

status = True
players = [Player('Connor'), Player('James'), Player('Rae')]
deck = Deck()
dealer = Dealer(deck, players)
stack = Stack()
dealer.deal()
game = Game(players)

# 1 - either
# 2 - only

rules = {
    "None": {
        'Default': True
    },
    "Suits": {
        "Spades": {
            'Default': False,
            'Spades': True,
            'Enforced': False
        },
        "Clubs": {
            'Default': False,
            'Clubs': True,
            'Enforced': False
        },
        "Diamonds": {
            'Default': False,
            'Diamonds': True,
            'Enforced': False
        },
        "Hearts": {
            'Default': False,
            'Hearts': True,
            'Enforced': False
        },
    },
    "Values": {
        "Ace": {
            'Default': False,
            'Ace': True,
            'Enforced': False
        },
        "Two": {
            'Default': False,
            'Two': True,
            'Enforced': True
        },
        "Three": {
            'Default': False,
            'Three': True,
            'Enforced': False
        },
        "Four": {
            'Default': False,
            'Four': True,
            'Enforced': True
        }
    }

}

while status:
    print("It is " + game.player_turn.name() + "'s turn")
    print(game.player_turn.name() + "'s Hand: " + game.player_turn.handAsStringList())
    if stack.top_card() is None:
        print('No cards in stack yet')
    else:
        print('Card at top of Stack is ' + stack.top_card().card_name())
    val = input("What card do you want to play?")
    game.player_turn.playCard(game.player_turn.get_card(val), stack)
    print('')
    print('')
    game.set_next_player_turn()


