# blackjack
A simple blackjack program in python.

So, we are going to use the below classes
class Hand
 Attributes:
    - Cards
 Methods:
    - handValue
    - isBlackJack
    
class Player
 Attributes:
    - Player Name
    - Player Balance
    - Table Number
    - Hand
 Methods:
    - addtoHand
    - addBalance
    - playTable - Assign this player to table # passed as argument
    - bet - Determine whether to bet and if so, for what amount?
    - hit - Determine whether to hit or stand?

class Blackjacktable
 Attributes:
    - Deck
    - Table number
    - Pot
    - Table Balance
    - Min Bet
    - Player(s)
    - Hand
 Methods:
    - addBalance
    - shuffle
    - deal - play the game
    - addPlayer
    - addtoHand - add card to the dealer's hand
    - hit - draw a card from the deck
