# +
import random
import drawblackjack.drawblackjack as dbj
from IPython.display import display, clear_output

#generate a random blackjack deck 
suit = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
rank = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
game_deck = []
for i in suit:
    for j in rank:
        game_deck.append((i, j))
        
val_dict = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Jack":10, "Queen":10, "King":10, "Ace":11}


# -
class Blackjack:
    
    def __init__(self, deck = game_deck.copy(), draw = False):
        self.deck = deck.copy()
        self.player = [] #Player's hand
        self.dealer = [] #Dealer's first two cards
        self.dealer_extra = [] #Extra dealer cards they pick up at the end
        
        self.shuffle()
        
        self.does_draw = draw
        self.is_active = True
        self.player_win = None
        
        if self.does_draw == True: #initalize display
            self.display = dbj.GameDisplay()
            
        for i in range(2): #deal cards to player
            c = self.deck.pop()
            self.player.append(c)
            if self.does_draw == True:
                self.display.add_player_card((c[1].lower(), c[0].lower())) #opposite format
                
        for i in ["up", "down"]: #deal cards to dealer
            c = self.deck.pop()
            self.dealer.append(c)
            if self.does_draw == True:
                self.display.add_dealer_card((c[1].lower(), c[0].lower()), i) #opposite format

        if self.does_draw == True:
            self.display.draw()
            
        if self.point(who = "dealer") == 21: #Game ends automatically if dealer draws 21
            self.end()
        
        if self.point() == 21: #Game ends automatically if player is dealt 21
            self.end()
            
    def shuffle(self):
        random.shuffle(self.deck)
    
    def hit(self):
        if self.is_active == False:
            raise Exception("Game is over")
        
        c = self.deck.pop()
        self.player.append(c)
        if self.does_draw == True:
            self.display.add_player_card((c[1].lower(), c[0].lower()))
            self.display.draw()

        if self.check_bust() == True:
            self.end(bust = True)
            
        if self.point() == 21:
            self.end()
            
    def end(self, bust = False):
        """End game. Return if player won or not"""
        points_p = self.point()
        points_d = self.point(who = "dealer")
        
        # Dealer stuff, hit up to 16, stay on 17
        
        while points_d < 17:
            c = self.deck.pop()
            self.dealer_extra.append(c)
            if self.does_draw == True:
                self.display.add_dealer_extra((c[1].lower(), c[0].lower())) #opposite format
            points_d = self.point(who = "dealer")
        
        self.is_active = False
        
        if points_d > 21:
            win = True
        if points_p > points_d:
            win = True
        else:
            win = False
            
        if bust == True:
            win = False
        
        if self.does_draw == True:
            clear_output()
            self.display.draw_gameover(win = win)
        
        if win == True:
            self.player_win = True
        else:
            self.player_win = False
            
        return win
        
    def stay(self):
        '''End the game'''
        if self.is_active == False:
            raise Exception("Game is over")
        
        self.end()

    def aces(self):
        """Returns number of aces in player's hand"""
        
        aces = 0
        for card in (self.player):
            val = card[1]
            if val == "Ace":
                aces += 1
                
        return aces
        
    def point(self, who = "player"):
        '''Check the player's points'''
        points = 0
        aces = 0
        if who == "player":
            for card in self.player:
                val = card[1]
                points += val_dict[val]
                if val == "Ace":
                    aces += 1
        elif who == "dealer":
            for card in (self.dealer + self.dealer_extra):
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
    
    def get_features(self):
        '''Return neural network features in proper format'''
        rnd = len(self.player) - 2
        return [[self.point(), self.aces(), val_dict[self.dealer[0][1]], rnd]]
