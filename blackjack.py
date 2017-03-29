import random
import time

class Hand(object):
    points = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'K':10, 'Q':10, 'J':10}
    
    def __init__(self,cards=[]):
        self.cards = cards

    def handValue(self):
        sum_cards=0
        for card in self.cards:
            sum_cards+=Hand.points[card]
        if 'A' in self.cards and sum_cards<21 and sum_cards+10<=21:
            sum_cards+=10
        return sum_cards 

    def __str__(self):
        return "{}".format(self.cards)
    
    def isBlackJack(self):
        return (self.handValue()==21 and 'A' in self.cards and len(self.cards) ==2)
 
 class Player(object):
    def __init__(self, name, hand=Hand(), balance=0, table=None):
        self.name = name
        self.hand = hand
        self.balance = balance
        self.table = table
        if type(table) == BlackjackTable:
            self.table.addPlayer(self)
    def __str__(self):
        return self.name
    
    def addtoHand(self,card):
        self.hand.cards.append(card)
        
    def addBalance(self,amt):
        self.balance+=amt
    
    def playTable(self,table):
        self.table = table
        self.table.addPlayer(self)
    
    def bet(self):
        play=''
        while play !='Y' and play != 'N':
            play=input("Hey {}, do you want to play [Y/N]? ".format(self.name)).upper()
        if play=='Y':
            if self.balance==0:
                print("Looks like you do not have any money. Please add money to play...")
                return 0
            amt=-1
            while True:
                try:
                    amt=float(input("How much do you want to bet (Balance: ${})? ".format(self.balance)))
                except ValueError as ex:
                    print ("Please enter a numeric value (xx.xx format)")
                else:
                    if amt>self.balance:
                        print ("You do not have sufficient balance to bet {}".format(amt))
                    else:
                        self.balance -= amt
                        return amt
        else:
            print("It was a pleasure playing Blackjack with you! Your balance is : {}".format(self.balance))
            return 0
        
    def hit(self):
        play=''
        while play !='H' and play != 'S':
            play=input("Hit or Stand [H/S] ? ").upper()
        return play=='H'

class BlackjackTable(object):
    gbldeck = ['A','2','3','4','5','6','7','8','9','10','K','Q','J']*4
    def __init__(self,table_id,balance=10000,pot=0,minbet=10,player=None,hand=Hand()):
        self.table_id = table_id
        self.balance = balance
        self.pot = pot
        self.minbet = minbet
        self.player = player
        self.hand = hand
        self.netbalance=0
        self.deck=BlackjackTable.gbldeck
    
    def __str__(self):
        return "{}'s hand: {}\t\tDealer's hand: {}".format(self.player,self.player.hand,self.hand)
    
    def addPlayer(self,player):
        self.player = player
    
    def addtoHand(self,card):
        self.hand.cards.append(card)
    
    def addBalance(self, amt):
        self.balance+=amt
    
    def sub_shuffle(self,deck):
        if len(deck)<=1:
            return deck
        rand=random.random()
        if (rand*10)%3 == 0:
            return self.sub_shuffle(deck[int(len(deck)*rand)+1:])+[deck[int(len(deck)*rand)]]+self.sub_shuffle(deck[:int(len(deck)*rand)])
        elif (rand*10)%3 == 1:
            return [deck[int(len(deck)*rand)]]+self.sub_shuffle(deck[:int(len(deck)*rand)])+self.sub_shuffle(deck[int(len(deck)*rand)+1:])
        else:
            return self.sub_shuffle(deck[:int(len(deck)*rand)])+self.sub_shuffle(deck[int(len(deck)*rand)+1:])+[deck[int(len(deck)*rand)]]
    
    def shuffle(self):
        for i in range(int(100*random.random()+10)):
            self.deck=self.sub_shuffle(self.deck)
        #print (self.deck)
    
    def hit(self):
        if len(self.deck)<14:
            print("Reshuffling...")
            self.deck=BlackjackTable.gbldeck
            self.shuffle()
            time.sleep(3)
        return self.deck.pop(0)
    
    def deal(self):
        if self.player == None:
            print("No player at the table :(")
            return -1
        else:
            # Unset hand if it exists
            self.hand=Hand([])
            self.player.hand=Hand([])
            self.shuffle()

            # See if the player wants to bet
            amt=self.player.bet()
            while amt>0:
                self.pot=amt
                card=self.hit()
                self.player.addtoHand(card)
                print ("Card {} dealt to player {}".format(card,self.player))
                
                card=self.hit()
                self.addtoHand(card)
                print ("Dealer has Card {}".format(card))
                
                card=self.hit()
                self.player.addtoHand(card)
                print ("Card {} dealt to player {}".format(card,self.player))
                print(self)
                if self.player.hand.isBlackJack():
                    print("Hey {}, Looks like you got a BlackJack!!".format(self.player))
                    print("You won ${}".format(amt*1.5))
                    self.balance-=amt*1.5
                    self.pot=0
                    self.player.addBalance(amt*2.5)
                player_hand=self.player.hand.handValue()
                card2=self.hit()
                # card2 is dealer's 2nd hidden card, which we'll reveal once player completes his moves
                # Hit/stand based on what the player wants to do until player busts or stops
                while (player_hand<21 and self.player.hit()):
                    card=self.hit()
                    self.player.addtoHand(card)
                    print ("Card {} dealt to player {}".format(card,self.player))
                    player_hand=self.player.hand.handValue()
                    print(self)
                    if self.player.hand.isBlackJack():
                        print("Hey {}, Looks like you got a BlackJack!!".format(self.player))
                        print("You won ${}".format(amt*1.5))
                        self.balance-=amt*1.5
                        self.pot=0
                        self.player.addBalance(amt*2.5)
                    elif player_hand>21:
                        print("Hey {}, Looks like you got busted".format(self.player))
                        self.balance+=self.pot
                        self.pot=0
                        
                    else:
                        print("Player {}: Hand value: {}".format(self.player,player_hand))
                        # Reveal the dealer's 2nd card 
                        self.addtoHand(card2)
                        print(self)
                
                # If Player is not busted already, hit/stand based on what the player wants to do
                if not self.player.hand.isBlackJack() and player_hand<=21:
                    while self.hand.handValue()<17:
                        #print ("Dealer's hand: {}".format(self.hand))
                        card=self.hit()
                        self.addtoHand(card)
                        time.sleep(1)
                        print(self)
                    if self.hand.handValue()>21 or player_hand>self.hand.handValue():
                        print("Hey {}, You won ${}".format(self.player,amt))
                        self.balance-=amt
                        self.pot=0
                        self.player.addBalance(amt*2)
                    elif player_hand==self.hand.handValue():
                        print("Hey {}, this game tied. You did not win anything.".format(self.player))
                        self.pot=0
                        self.player.addBalance(amt)
                    else:
                        print("Hey {}, you lost this game. Better luck next time.".format(self.player))
                        self.balance+=self.pot
                        self.pot=0
                self.hand=Hand([])
                self.player.hand=Hand([])
                amt=self.player.bet()
            print("Table balance: {}".format(self.balance))

