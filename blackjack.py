import random

#REPRESENTS THE CARDS OF A DECK
class Card:
    def __init__(self,suit,number):
        self.suit = suit
        self.number = number
    
    
    #names the cards
    #used for splitting and for future display
    def get_card(self): 
        if self.number == 1:
            return "ace"
        if self.number == 11:
            return "jack"
        if self.number == 12:
            return "queen"
        if self.number == 13:
            return "king"
        return self.number
        
        
    #gets the value for the cards to add up the total value
    def get_val(self):
        if self.number > 10:
            return 10
        else:
            return self.number
    
    #checks if the card is an ace
    def is_ace(self):
        return self.number == 1
        
        
    #overrides add operator so can add cards together
    def __add__(self, other):
        return self.number.get_val() + other.number.get_val()
    
    
#REPRESENTS EACH DECK
class Deck:
    def __init__(self):
        self.deck = []
        for x in range(1,14):
            self.deck.append(Card("Heart", x))
            self.deck.append(Card("Club", x))
            self.deck.append(Card("Diamond", x))
            self.deck.append(Card("Spade", x))
            
    #picks the card at random from the deck
    def pick_card(self):
        return self.deck.pop(random.randint(0,len(self.deck)-1))
        
    #checks if the deck is empty
    def is_empty(self):
        return len(self.deck) < 1
    
#REPRESNTS THE CURRENT GAME OF BLACKJACK
class Game:
    def __init__(self, rule1, rule2 , decks, bal): #done
        self.rule1 = rule1
        self.rule2 = rule2
        self.decks = []
        self.bal = bal
        self.playing_amt = 0
        for x in range(decks):
            self.decks.append(Deck())
        
    #picks the card from a random deck
    #checks that there is a deck that is not empty to pick from
    def pick_card(self):
        avail_decks = []
        for x in range(len(self.decks)):
            if not self.decks[x].is_empty():
                avail_decks.append(x)
        if len(avail_decks) == 0:
            raise Exception("No more cards")
        rand = random.randint(0, len(avail_decks)-1)
        return self.decks[rand].pick_card()
        
    #plays a hand of blackjack
    def play_hand(self):
        first_move = True
        self.playing_amt = int(input("How much do you want to bet on this hand?"))
        can_double = True
        your_hand = []
        dealers_hand = []
        if self.bal < (2*self.playing_amt) + 1:
            can_double = False
        your_hand.append(self.pick_card())
        your_hand.append(self.pick_card())
        dealers_hand.append(self.pick_card())
        dealers_hand.append(self.pick_card())
        print("your hand is " + str(your_hand[0].get_card()) + " " + "and " + str(your_hand[1].get_card()))
        print("the dealer is showing " + str(dealers_hand[0].get_card()))
        
        #insurance for player and checks if dealer has blackjack
        if dealers_hand[0].is_ace():
            insurance = input("Would you like to buy insurance? (Y/N)")
            if insurance == "Y" and dealers_hand[1].get_val() == 10:
                print("dealer had blackjack, insurance was good")
                self.hand_end_print(dealers_hand, your_hand)
                print("you have " + str(self.bal) + " dollars")
                return 0
            elif insurance == "Y" and not dealers_hand[1].get_val() == 10:
                self.bal = self.bal - (self.playing_amt/2)
                print("dealer did not have blackjack")
                print("you have " + str(self.bal) + " dollars")
            elif insurance == "N" and dealers_hand[1].get_val() == 10:
                self.hand_end_print(dealers_hand, your_hand)
                print("you lose")
                print("you have " + str(self.bal) + " dollars")
                return -1
            
        # checks for blackjack for player
        if (your_hand[0].is_ace() or your_hand[1].is_ace()) and (your_hand[0].get_val() == 10 or your_hand[1].get_val() == 10):
            self.bal = self.bal + (self.playing_amt * 1.5)
            self.hand_end_print(dealers_hand, your_hand)
            print("black jack you win")
            print("you have " + str(self.bal) + " dollars")
            return 1
        
        #checks if player can split the hand
        if your_hand[0].get_card() == your_hand[1].get_card():
            split = True
        else:
            split = False
            
        your_hand = self.mover(split, first_move, can_double, dealers_hand, your_hand)  
        
        return self.check_dealer(dealers_hand, your_hand)
            

    
    def move_hit(self, dealers_hand, your_hand):
        your_hand.append(self.pick_card())
        print("You drew a " + str(your_hand[-1].get_card()))
        self.print_hand(your_hand)   
        tot = self.value_of_hand(your_hand)
        if not (isinstance(tot,list) or tot < 22):
            return -1
        
    
    def move_split(self, your_hand, dealers_hand):
        split_hand = [[],[]]
        split_hand[0].append(your_hand[0])
        split_hand[0].append(self.pick_card())
        split_hand[1].append(your_hand[1])
        split_hand[1].append(self.pick_card())
        return self.splitter_helper(split_hand[0], split_hand[1], dealers_hand)
        
    def splitter_helper(self, hand1, hand2, dealers_hand): # need to think how double works for this
        self.print_hand(hand1)
        if hand1[0].get_card() == hand1[1].get_card():
            split1 = True
        else:
            split1 = False
        if hand2[0].get_card() == hand2[1].get_card():
            split2 = True
        else:
            split2 = False
        can_double = True
        if self.bal < (2*self.playing_amt) + 1:
            can_double = False
        hand1 = self.mover(split1, True, can_double, dealers_hand, hand1)
        self.print_hand(hand2)
        hand2 = self.mover(split2, True, can_double, dealers_hand, hand2)
        new_hand = [hand1, hand2]
        print(new_hand)
        return new_hand
        
    #function for stand if move is stand for rule S17
    def check_dealer(self, dealers_hand, your_hand):
        #while loop for the base case of less than 17
        
        if isinstance(your_hand[0],list):
            return self.check_dealer_splitter(your_hand, dealers_hand)
            #FOR THE SPLITTTER
        deal_value = self.value_of_hand(dealers_hand)
        rule = 17
        if self.rule1 == "H":
            rule = 18
        tot = self.value_of_hand(your_hand) 
        if self.optimal_value(tot) > 21:
            self.bal = self.bal - self.playing_amt
            self.hand_end_print(dealers_hand, your_hand)
            print("You are over 21, you lose")
            print("you have " + str(self.bal) + " dollars")
            return -1
        while isinstance(deal_value, list) or deal_value < 17:
            
            #deal value to see if there is an ace ever in the hand -- noted when it is a list
            
            if isinstance(deal_value, list):
                # if list, means theres an ace, therefore draw differently
                while deal_value[0] < 17 and (deal_value[1] < rule or deal_value[1] > 21):
                    dealers_hand.append(self.pick_card())
                    deal_value = self.value_of_hand(dealers_hand)
                
                break
                
                
            dealers_hand.append(self.pick_card())
            deal_value = self.value_of_hand(dealers_hand)
            
            
        if self.optimal_value(self.value_of_hand(dealers_hand)) > 21:
            self.bal = self.bal + self.playing_amt
            self.hand_end_print(dealers_hand, your_hand)
            print("you win")
            print("you have " + str(self.bal) + " dollars")
            return 1
        elif self.optimal_value(self.value_of_hand(dealers_hand)) < 22 and self.optimal_value(self.value_of_hand(dealers_hand)) > self.optimal_value(self.value_of_hand(your_hand)):
            self.hand_end_print(dealers_hand, your_hand)
            print("you lose")
            self.bal = self.bal - self.playing_amt
            print("you have " + str(self.bal) + " dollars")
            return -1
        elif self.optimal_value(self.value_of_hand(dealers_hand)) < 22 and self.optimal_value(self.value_of_hand(dealers_hand)) < self.optimal_value(self.value_of_hand(your_hand)):
            self.bal = self.bal + self.playing_amt 
            self.hand_end_print(dealers_hand, your_hand)
            print("you win")
            print("you have " + str(self.bal) + " dollars")
            return 1
        elif self.optimal_value(self.value_of_hand(dealers_hand)) < 22 and self.optimal_value(self.value_of_hand(dealers_hand)) == self.optimal_value(self.value_of_hand(your_hand)):
            self.hand_end_print(dealers_hand, your_hand)
            print("push")
            print("you have " + str(self.bal) + " dollars")
            return 0
            
   
    def check_dealer_splitter(self, your_hand, dealers_hand):
        if isinstance(your_hand[0], list):
            self.check_dealer_splitter(your_hand[0], dealers_hand)
        if isinstance(your_hand[1], list):
            self.check_dealer_splitter(your_hand[1], dealers_hand)
        if not isinstance(your_hand[0], list) and not isinstance(your_hand[1], list):
            self.check_dealer(dealers_hand, your_hand)
            
    #gets balance of the player
    def get_bal(self):
        return self.bal
    
    #helper for value_of_hand for addition
    def sum_of_hand(self, hand):
        s = 0
        for x in hand:
            s += x.get_val()
        return s
        
    #gets the value of the hand, if ace, splits into needed numbers 
    def value_of_hand(self, hand):
        ace = False
        for x in hand:
            if x.is_ace():
                ace = True
            
        if ace and self.sum_of_hand(hand) < 22:
            return [self.sum_of_hand(hand), self.sum_of_hand(hand) + 10]
        else:
            return self.sum_of_hand(hand)
            
    #if theres a list of values due to an ace, it gets the optimal value for S17 rules
    def optimal_value(self, value_list):
        if self.rule1 == "S":
            val = 16
        else:
            val = 17
        if isinstance(value_list, int):
            return value_list
        if value_list[1] > val and value_list[1] < 22:
            return value_list[1]
        else:
            return value_list[0]

    #prints the hand at the end
    def hand_end_print(self, dealers_hand, your_hand):
        print("The dealer has ", end="")
        for x in dealers_hand:
            print(str(x.get_card()),end= " ")
        print("")
        print("You have ", end="")
        for x in your_hand:
            print(str(x.get_card()), end=" ")
        print("")
        
    def print_hand(self, hand):
        print("Your hand is now ", end="")
        for x in hand:
            print(x.get_card(), end= " ")
        print("") 
        
    #determines the next move of the player based on the rules    
    def next_move(self, split, first_move, can_double):
        if can_double:
            if self.rule2 == "Y" and first_move and split:
                x = input("Will you stand, surrender, double, hit or split (ST/SU/D/SP/H)")
                while not (x == "ST" or x == "SU" or x == "D" or x == "SP" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand, surrender, double, hit or split (ST/SU/D/SP/H)")
            elif self.rule2 == "Y" and not first_move and split:
                x = input("Will you stand, hit or split (ST/SP/H)")
                while not (x == "ST" or x == "SP" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand, hit or split (ST/SP/H)")
            elif self.rule2 == "Y" and not first_move and not split:
                x = input("Will you stand, hit (ST/H)")
                while not (x == "ST" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand, hit or split (ST/H)")
            elif self.rule2 == "Y" and first_move and not split:
                x = input("Will you stand, surrender, double, hit (ST/SU/D/H)")
                while not (x == "ST" or x == "SU" or x == "D" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand, surrender, double or hit (ST/SU/D/H)")
            elif self.rule2 == "N" and first_move and split:
                x = input("Will you stand, double, hit or split (ST/D/SP/H)")
                while not (x == "ST" or x == "D" or x == "SP" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand, double, hit or split (ST/D/SP/H)")
            elif self.rule2 == "N" and not first_move and split:
                x = input("Will you stand, hit or split (ST/SP/H)")
                while not (x == "ST" or x == "SP" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand,hit or split (ST/SP/H)")
            elif self.rule2 == "N" and not first_move and not split:
                x = input("Will you stand, hit (ST/H)")
                while not (x == "ST" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand or hit (ST/H)")
            elif self.rule2 == "N" and first_move and not split:
                x = input("Will you stand, double, hit (ST/D/H)")
                while not (x == "ST" or x == "D" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand, double, hit (ST/D/H)")
        else:
            if self.rule2 == "Y" and first_move and split:
                x = input("Will you stand, surrender,  hit or split (ST/SU/SP/H)")
                while not (x == "ST" or x == "SU"  or x == "SP" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand, surrender, hit or split (ST/SU/SP/H)")
            elif self.rule2 == "Y" and not first_move and split:
                x = input("Will you stand, hit or split (ST/SP/H)")
                while not (x == "ST" or x == "SP" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand, hit or split (ST/SP/H)")
            elif self.rule2 == "Y" and not first_move and not split:
                x = input("Will you stand, hit (ST/H)")
                while not (x == "ST" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand, hit or split (ST/H)")
            elif self.rule2 == "Y" and first_move and not split:
                x = input("Will you stand, surrender, hit (ST/SU/H)")
                while not (x == "ST" or x == "SU" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand, surrender or hit (ST/SU/H)")
            elif self.rule2 == "N" and first_move and split:
                x = input("Will you stand, hit or split (ST/SP/H)")
                while not (x == "ST" or x == "SP" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand, hit or split (ST/SP/H)")
            elif self.rule2 == "N" and not first_move and split:
                x = input("Will you stand, hit or split (ST/SP/H)")
                while not (x == "ST" or x == "SP" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand,hit or split (ST/SP/H)")
            elif self.rule2 == "N" and not first_move and not split:
                x = input("Will you stand, hit (ST/H)")
                while not (x == "ST" or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand or hit (ST/H)")
            elif self.rule2 == "N" and first_move and not split:
                x = input("Will you stand, hit (ST/H)")
                while not (x == "ST"  or x == "H"):
                    print("Try again, that is not an option")
                    x = input("Will you stand, hit (ST/H)")
        return x
        
    def mover(self, split, first_move, can_double, dealers_hand, your_hand):
        move = ""
        end = 0
        while not move == "D" and not end == -1:    
            #gets the move of the player
            move = self.next_move(split, first_move, can_double)
            
            #checks if the move is surrender
            if move == "SU":
                self.bal = self.bal + (self.playing_amt/2)
                print("You surrendered")
                print("you have " + str(self.bal) + " dollars")
                return -0.5
            
            
            #checks if the move is stand, probably can make this a function
            elif move == "ST":
                break
                #return self.move_stand(dealers_hand, your_hand, playing_amt)
        
            elif move == "H" or move == "D":
                first_move = False
                if move == "D":
                    self.playing_amt = self.playing_amt * 2
                end = self.move_hit(dealers_hand, your_hand)
                # more moves after
        
            elif move == "SP": # need work ON THISSSSSSSSSSSSSSSSSSS
                end = self.move_split(your_hand, dealers_hand)
                return end 
                # more moves after
        return your_hand
        
            
class Start:
    def __init__(self):
        self.rule1 = input("Is this H or S 17")
        self.rule2 = input("Is this surrender of not (Y/N)")
        self.decks = int(input("How many decks are you using?"))
        self.bal = int(input("How much is your staring balance?"))
        self.game = Game(self.rule1, self.rule2 , self.decks, self.bal)
        
    #plays the game
    def play_game(self):
        total = 0
        cont = "Y"
        while cont == "Y" and self.game.get_bal() > 0:
            wins = self.game.play_hand();
            total += 1
            if self.game.get_bal() < 0:
                raise Excpetion("You are out of money")
            
            cont = input("Would you like to play another hand? (Y/N)")
        print("You ended the game with " + str(self.game.get_bal()))
        print("You gained " + str(self.game.get_bal() - self.bal))
        print("You played a total of " + str(total) + " games")
        print("Net win of " + str(wins) + " games")
        
             
        
start = Start()
start.play_game()


        



