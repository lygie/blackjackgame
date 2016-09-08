# Mini-project #6 - Blackjack
# http://www.codeskulptor.org/#user18_jEJLhJZrYS_93.py
import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
dealVal = '?'
playVal = ''
newdeal = ''



# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.handList = []
            

    def __str__(self):
        
        return 'Hand Contains:'+','.join([card.get_suit() + card.get_rank() for card in self.handList])    
    def add_card(self, card):
        self.handList.append(card)	# add a card object to a hand
        
        
 
        
    def get_value(self):
        total = 0
        ace = False
        for each in self.handList:
            if each.get_rank() not in ['A', 'T', 'J', 'K', 'Q']:
                total += VALUES[each.get_rank()]
            if each.get_rank() in ['T', 'J', 'K', 'Q']:
                total += 10
            if each.get_rank() == 'A':
                total += 1
                ace = True
        if total + 10 <= 21 and ace:
            return total + 10
        else:
            return total
                
        
        
        
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        for i in self.handList:
            i.draw(canvas,pos)
            pos[0] += 90
        
# define deck class 
class Deck:
    def __init__(self):
        self.deckList = []
        for i in SUITS:
            for j in RANKS:
                self.deckList.append(Card(i,j))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deckList)

    def deal_card(self):
        return self.deckList.pop()
    
    def __str__(self):
        for d in self.deckList:
            return 'Deck contains: '+','.join([d.get_suit() + d.get_rank() for d in self.deckList])
deck = Deck()
player = Hand()
dealer = Hand()
outcome = ''


#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer,deck, hand, score, playVal, dealVal, newdeal
    
    playVal = ''
    dealVal = '?'
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    outcome = 'Would you like to hit or stand?'
    newdeal = ''
    
    if in_play:
        outcome = 'Pressing deal during play loses!'
        score -= 10
    
    # your code goes here
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    playVal = str(player.get_value())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    in_play = True

def hit():
    global outcome, in_play, player, dealer,deck, hand, score,playVal, newdeal

    if in_play:
        player.add_card(deck.deal_card())
        playVal = str(player.get_value())
        if player.get_value() >21:
            outcome = "You Busted!"
            newdeal = "Would you like a new deal?"
            in_play = False
            score -=10
    else:
        outcome = "Please deal a new game!"
            
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global outcome, in_play, player, dealer,deck, hand, score, dealVal, playVal, newdeal
    
    if in_play:
        while dealer.get_value() <= 17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            outcome = "Dealer Busted! You win!!"
            newdeal = "Would you like a new deal?"
            score += 10
        else:
            newdeal = "Would you like a new deal?"
            if dealer.get_value() >= player.get_value():
                outcome = "Sorry, you lose!"
                score -= 10
                
            else:
                outcome = "Congratulations!! You win!!"
                score += 10
        dealVal = str(dealer.get_value())
    in_play = False
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('Score: '+ str(score), [400,100],32,"Maroon")
    canvas.draw_text("BlackJack", [70,100], 38, "Black")
    canvas.draw_text('Player:', [70,380], 25, "Navy")
    canvas.draw_text(playVal,[140,380],25, "Navy")
    canvas.draw_text(outcome, [220,180], 25, "Navy")
    canvas.draw_text('Dealer:', [70,180],25, "Navy")
    canvas.draw_text(dealVal, [145,180], 25, "Navy")
    canvas.draw_text(newdeal, [140, 550], 25, "Maroon")
    player.draw(canvas,[50,400])
    dealer.draw(canvas,[50,200])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,[51 + CARD_BACK_CENTER[0], 201 + CARD_BACK_CENTER[1]],CARD_BACK_SIZE)
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
frame.start()



# remember to review the gradic rubric