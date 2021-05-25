# Imports
import random

# Constants
suits = ["Suns", "Swords", "Cups", "Bastoni"]
ranks = [["Ace", 11, 10], ["3", 10, 9], ["King", 4, 8], ["Horseman", 3, 7], ["Queen", 2, 6], ["7", 0, 5], ["6", 0, 4], ["5", 0, 3], ["4", 0, 2], ["2", 0, 1]]

class Card:

    def __init__(self, suit, rank, value, intRank):
        self.suit = suit
        self.rank = rank
        self.value = value
        self.intRank = intRank

class Deck:

    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank[0], rank[1], rank[2])
                self.cards.append(card)
        random.shuffle(self.cards)
    
    def shuffle(self):
        random.shuffle(self.cards)

    def count(self):
        return len(self.cards)

class Player:

    def __init__(self):
        self.score = 0
        self.hand = []

    def play_card(self, index):
        return self.hand.pop(index)

    def print_hand(self):
        print("{:8s} {:9s} {:2s}".format("Suit", "Rank", "Value"))
        print("-" * 24)
        for i in range(len(self.hand)):
            card = self.hand[i]
            print("{:8s} {:9s} {:2d}".format(card.suit, card.rank, card.value))
    
    def count(self):
        return len(self.hand)

class Game:

    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.deck = Deck()
        for i in range(3):
            self.player1.hand.append(self.deck.cards.pop())
            self.player2.hand.append(self.deck.cards.pop())
        self.briscola = self.deck.cards.pop()
        self.deck.cards.insert(0, self.briscola)

    def deal_card(self, player1, player2):
        player1.hand.append(self.deck.cards.pop())
        player2.hand.append(self.deck.cards.pop())

    def card_cmp(self, card1, card2):
        if card1.suit == self.briscola.suit:
            if card2.suit == self.briscola.suit:
                if card1.intRank > card2.intRank:
                    winner = 1
                else:
                    winner = 2
            else:
                winner = 1
        elif card2.suit == self.briscola.suit:
            if card1.suit == self.briscola.suit:
                if card1.intRank > card2.intRank:
                    winner = 1
                else:
                    winner = 2
            else:
                winner = 2
        elif card1.suit == card2.suit:
            if card1.intRank > card2.intRank:
                winner = 1
            else:
                winner = 2
        else:
            winner = 1
        
        return winner

class Bot:

    def __init__(self, player, game):
        self.player = player
        self.game = game
        self.memory = {
            "Suns": [None]*10,
            "Swords": [None]*10,
            "Cups": [None]*10,
            "Bastoni": [None]*10
        }
        for i in range(3):
            self.memory_insert(self.player.hand[i])

    def make_move(self, oppositionCard=None):
        worstCard = self.worst_card()
        if oppositionCard:
            up = self.suit_in_deck(oppositionCard.suit, oppositionCard.intRank)
            worstBrisc = self.worst_brisc()
            if self.game.player1.score >= 50:
                dire_factor = 2
            elif self.game.player1.score >= 39:
                dire_factor = 3
            else:
                dire_factor = 4
            if oppositionCard.suit == self.game.briscola.suit:
                index = worstCard
            elif up:
                index = up
            elif (oppositionCard.value >= dire_factor) and (worstBrisc != None) and (self.player.hand[worstBrisc].value <= oppositionCard.value):
                index = worstBrisc
            elif (worstBrisc != None) and (self.player.hand[worstBrisc].value < 2) and (self.player.hand[worstCard].value > dire_factor):
                index = worstBrisc
            else:
                index = worstCard
        else:
            ub = self.unbeatable_card()
            if ub:
                index = ub
            else:
                index = worstCard

        return index
            
                

    def suit_in_deck(self, target_suit, min_rank):
        handCount = self.player.count()
        index = None
        for i in range(handCount):
            currentCard = self.player.hand[i]
            if index and currentCard.suit == target_suit:
                benchmarkCard = self.player.hand[index]
                if (currentCard.value >= benchmarkCard.value) and (currentCard.intRank > benchmarkCard.intRank):
                    index = i
            elif (currentCard.suit == target_suit) and (currentCard.intRank >= min_rank):
                index = i
        return index

    def worst_card(self):
        handCount = self.player.count()
        index = handCount-1
        for i in range(handCount):
            currentCard = self.player.hand[i]
            benchmarkCard = self.player.hand[index]
            if currentCard.suit != self.game.briscola.suit:
                if benchmarkCard.suit == self.game.briscola.suit:
                    index = i
                elif (benchmarkCard.value >= currentCard.value) and (benchmarkCard.intRank > currentCard.intRank):
                    index = i
            else:
                if (benchmarkCard.suit == self.game.briscola.suit) and (benchmarkCard.value >= currentCard.value) and (benchmarkCard.intRank > currentCard.intRank):
                    index = i

        return index

    def worst_brisc(self):
        handCount = self.player.count()
        index = None
        for i in range(handCount):
            currentCard = self.player.hand[i]
            if index:
                benchmarkCard = self.player.hand[index]
                if (currentCard.suit == self.game.briscola.suit) and (benchmarkCard.value >= currentCard.value) and (benchmarkCard.intRank > currentCard.intRank):
                    index = i
            elif currentCard.suit == self.game.briscola.suit:
                index = i

        return index

    def memory_insert(self, card):
        self.memory[card.suit][10-card.intRank] = card

    def unbeatable_card(self):
        handCount = self.player.count()
        index = None
        for i in range(handCount):
            currentCard = self.player.hand[i]
            if (currentCard.suit != self.game.briscola.suit):
                if index:
                    benchmarkCard = self.player.hand[index]
                    if currentCard.intRank > benchmarkCard.intRank:
                        memList = self.memory[currentCard.suit]
                        highest = True
                        for j in range(10-currentCard.intRank):
                            if memList[j] == None:
                                highest = False
                                break
                        if highest == True:
                            index = i
                else:
                    memList = self.memory[currentCard.suit]
                    highest = True
                    for j in range(10-currentCard.intRank):
                        if memList[j] == None:
                            highest = False
                            break
                    if highest == True:
                        index = i
        
        return index