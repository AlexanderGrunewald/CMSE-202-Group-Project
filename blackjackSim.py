# +
#generate a random blackjack deck 
import random
suit = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
rank = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
deck = []
for i in suit:
    for j in rank:
        deck.append((i, j))
        
val_dict = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Jack":10, "Queen":10, "King":10, "Ace":11}
# -



class Blackjack:
    
    def __init__(self, deck):
        self.deck = deck
        self.player = []
        self.dealer = []
        
        self.shuffle()
        self.dealer.append(self.deck.pop())
        self.dealer.append(self.deck.pop()) #twice
        
        self.player.append(self.deck.pop())
        self.player.append(self.deck.pop())
        
        self.is_active = True
        
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def hit(self):
        self.player.append(self.deck.pop())

        if self.check_bust() == True:
            self.end(bust = True)
            
    def end(self, bust = False):
        """End game. Return if player won or not"""
        points_p = self.point()
        points_d = self.point(who = "dealer")
        
        self.is_active = False
        
        if bust == True:
            return False
        
        if points_p > points_d:
            return True
        else:
            return False
        
    def stay(self):
        '''End the game'''
        self.end()

    def point(self, who = "player"):
        '''Check the points'''
        points = 0
        aces = 0
        if who == "player":
            for card in self.player:
                val = card[1]
                points += val_dict[val]
                if val == "Ace":
                    aces += 1
        elif who == "dealer":
            for card in self.dealer:
                val = card[1]
                points += val_dict[val]
                if val == "Ace":
                    aces += 1
            
        #aces are counted as 11, here we see if any should be counted as 1
        while points > 21 and aces > 0:
            points -= 10
            aces -= 1
                
        return points

    def check_bust(self):
        '''Check if the player is bust'''
        points_p = self.point()
        if points_p > 21:
            return True
        else:
            return False
        

    def reset(self):
        '''Reset the game'''
        self.__init__()
        pass
    
    def play(self):
        '''Play the game and collect data'''
        pass

game = Blackjack(deck)
game.point()

# +
# input?
# -


    

# +
#run the game
n = 1000
win = [] #label
ace = []
point = []
dealer_card = []
player_card = []
hit = [] #(0 for stay, 1 for hit)

for i in range(n):
    game = Blackjack(deck)
    hits = 0
    point.append(game.point())
    dealer_card.append(game.dealer[0][1])
    player_card.append()
    
    while game.is_active == True:
        if random.random > 0.5:
            game.hit()
            hits += 1
        else:
            game.stay()

    if game.is_active == False:
        hit.append(hits)
            
