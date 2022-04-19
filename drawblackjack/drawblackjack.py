# +
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#Dictionaries for standardizing card input and fetching card locations on the board

card_dict = {2:"2", "two":"2", "2":"2",
            3:"3", "three":"3", "3":"3",
            4:"4", "four":"4", "4":"4",
            5:"5", "five":"5", "5":"5",
            6:"6", "six":"6", "6":"6",
            7:"7", "seven":"7", "7":"7",
            8:"8", "eight":"8", "8":"8",
            9:"9", "nine":"9", "9":"9",
            10:"10", "ten":"10", "10":"10",
            "jack":"j", "queen":"q", "q":"q", "j":"j",
            "king":"k", "ace":"a", "k":"k", "a":"a"}

suit_dict = {"spade":"spade", "spades":"spade",
            "heart":"heart", "hearts":"heart",
            "club":"club", "clubs":"club",
            "diamond":"diamond", "diamonds":"diamond"}

p_card_loc_dict = {0:[], 
                   1:[(367, 100)],
                   2:[(349, 100), (386, 100)],
                   3:[(330, 100), (367, 100), (404, 100)],
                   4:[(330, 100), (367, 100), (404, 100), (367, 149)],
                   5:[(330, 100), (367, 100), (404, 100), (349, 149), (386, 149)],
                   6:[(330, 100), (367, 100), (404, 100), (330, 149), (367, 149), (404, 149)]}

d_card_loc_dict = {0:[],
                   1:[(97, 149)],
                   2:[(79, 149), (116, 149)],
                   3:[(60, 149), (97, 149), (134, 149)]}

try:
    img = mpimg.imread("8BitDeckAssets.png")
except:
    img = mpimg.imread("drawblackjack/8BitDeckAssets.png")
try:
    bimg = mpimg.imread("gameboard.png")
except:
    bimg = mpimg.imread("drawblackjack/gameboard.png")
try:
    wlimg = mpimg.imread("winlosstext.png")
except:
    wlimg = mpimg.imread("drawblackjack/winlosstext.png")

    
    
class GameDisplay():
    def __init__(self):
        self.player_cards = []
        self.player_card_count = 0
        self.dealer_cards = {"up":None, "down":None}
        self.dealer_extra = []
        self.card_img = img
        self.ref_img = bimg.copy()          #unchanging, used to redraw
        self.board_img = bimg.copy()        #changing
        self.deck_color = "red"
        
    def validate_card_(self, card):
        """
        Returns a card with the correctly formatted strings for idenfication. 
        Input must be a tuple of strings ('value', 'suit')
        """
        if (isinstance(card, tuple) and len(card) == 2) == False:
            raise Exception("'card' should be a tuple of length 2: (value, suit)")
        if (card[0] in card_dict) == False:
            raise Exception("Please provide a valid card")
        if (card[1] in suit_dict) == False:
            raise Exception("Please provide a valid suit")
        return (card_dict[card[0]], suit_dict[card[1]])
        
    def add_dealer_card(self, card, facing):
        """
        Adds/changes the dealer's cards one at a time, specifying between the face-up and face-down ones.
        card: tuple of strings | (value, suit)
        facing: str | "up", "down"
        """
        if (facing in ["up", "down"]) == False:
            raise Exception("'facing' must be 'up' or 'down'")
            
        c = self.validate_card_(card)
        self.dealer_cards[facing] = c
        
    def add_dealer_extra(self, card):
        """
        Add to the dealer's extra cards. Should only be used at the end of the game
        card: tuple of strings | (value, suit)
        facing: str | "up", "down"
        """
        if len(self.dealer_extra) >= 3:
            raise Exception("Dealer can't draw more than 3 extra")
            
        c = self.validate_card_(card)
        self.dealer_extra.append(c)
        
    def add_player_card(self, card):
        """
        Gives the player a card
        card: tuple of strings | (value, suit)
        """
        if len(self.player_cards) >= 6:
            raise Exception("Can't draw more than 6 cards!")
        c = self.validate_card_(card)
        self.player_cards.append(c)
        self.player_card_count = len(self.player_cards)
        
    def change_deck_color(self):
        """
        Toggles the color of the back of the cards between blue and red
        """
        if self.deck_color == "red":
            self.deck_color = "blue"
        elif self.deck_color == "blue":
            self.deck_color = "red"
            

    def get_card_ary_(self, card):
        """
        Returns the image array of the specified card
        """
        val = card[0]
        suit = card[1]
        column = {"2":1, "3":2, "4":3, "5":4, "6":5, "7":6, "8":7, "9":8, "10":9, "j":10, "q":11, "k":12, "a":13}[val]
        row = {"heart":0, "club":1, "diamond":2, "spade":3}[suit]
        pr = 1 + 47*row
        pc = 1 + 35*column
        return self.card_img[pr:pr+45, pc:pc+33]
    
    def place_card_(self, ary, x, y):
        """
        Places card at pixel location (x, y) on board, top left being (0, 0).  
        """
        try:
            self.board_img[y:y+45, x:x+33] = ary
        except:
            raise Exception("'ary' must be a 33x45 pixel image array. Try using output from GameBoard.get_card_ary_()")
            
    def draw(self):
        """
        Draws the current state of the board using matplotlib.
        """
        self.board_img = self.ref_img.copy()
        
        for ci in range(self.player_card_count):
            ary = self.get_card_ary_(self.player_cards[ci])
            x = p_card_loc_dict[self.player_card_count][ci][0]
            y = p_card_loc_dict[self.player_card_count][ci][1]
            self.place_card_(ary, x, y)
            
        ary = self.get_card_ary_(self.dealer_cards["up"])
        self.place_card_(ary, 92, 100)
        
        if self.deck_color == "red":
            ary = self.card_img[1:46, 1:34]
        elif self.deck_color == "blue":
            ary = self.card_img[48:93, 1:34]
        self.place_card_(ary, 129, 100)
        
        plt.figure(figsize = (12, 15))
        plt.axis("off")
        plt.imshow(self.board_img)
        
    def draw_gameover(self, win):
        """
        Similar to draw(), but reveals the dealer's facedown card and a victory message 
        """
        self.board_img = self.ref_img.copy()
        
        for ci in range(self.player_card_count):
            ary = self.get_card_ary_(self.player_cards[ci])
            x = p_card_loc_dict[self.player_card_count][ci][0]
            y = p_card_loc_dict[self.player_card_count][ci][1]
            self.place_card_(ary, x, y)
            
        ary = self.get_card_ary_(self.dealer_cards["up"])
        self.place_card_(ary, 92, 100)
        ary = self.get_card_ary_(self.dealer_cards["down"])
        self.place_card_(ary, 129, 100)
        
        for ci in range(len(self.dealer_extra)):
            ary = self.get_card_ary_(dealer_extra[ci])
            x = d_card_loc_dict[len(self.dealer_extra)][ci][0]
            y = d_card_loc_dict[len(self.dealer_extra)][ci][1]
            self.place_card_(ary, x, y)
            
        if win == True:
            self.board_img[32:52, 195:303] = wlimg[:20, :108]
        elif win == False:
            self.board_img[32:51, 186:313] = wlimg[20:39, :127]
        
        plt.figure(figsize = (12, 15))
        plt.axis("off")
        plt.imshow(self.board_img)
