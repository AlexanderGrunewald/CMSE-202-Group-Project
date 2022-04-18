#generate a random blackjack deck 
import random
suit = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
rank = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
deck = []
for i in suit:
    for j in rank:
        deck.append(j + ' of ' + i)

class Blackjack:
    
    def __init__(self, deck):
        self.deck = deck
        self.player = []
        self.dealer = []
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def hit(self):
        self.player.append(self.deck.pop())
        
    def stay(self):
        '''End the game'''
        pass

    def point(self):
        '''Check the point of the player'''
        pass

    def check_bust(self):
        '''Check if the player is bust'''
        pass

    def reset(self):
        '''Reset the game'''
        pass
    
    def play(self):
        '''Play the game and collect data'''
        pass

    


    

