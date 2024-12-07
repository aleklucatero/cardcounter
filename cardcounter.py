import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import random

# Card Class
class Card:
    def __init__(self, val, suit):
        self.val = val
        self.suit = suit

# Dealer Class
class Dealer:
    def __init__(self):
        self.hand = []

    def draw(self, deck):
        card = deck.draw()
        self.hand.append(card)

    def reset(self):
        self.hand = []

    def score(self):
        ace_count = 0
        score = 0

        for card in self.hand:
            if card.val == 1:
                ace_count += 1
                score += 11
            elif card.val >= 10:
                score += 10
            else:
                score += card.val

        while score > 21 and ace_count > 0:
            score -= 10
            ace_count -= 1

        return score

# Player Class
class Player:
    def __init__(self):
        self.hand = []
        self.chips = 0

    def draw(self, deck):
        card = deck.draw()
        self.hand.append(card)

    def add_chips(self, amount):
        self.chips += amount

    def lose_chips(self, amount):
        self.chips -= amount

    def reset(self):
        self.hand = []

    def score(self):
        ace_count = 0
        score = 0

        for card in self.hand:
            if card.val == 1:
                ace_count += 1
                score += 11
            elif card.val >= 10:
                score += 10
            else:
                score += card.val

        while score > 21 and ace_count > 0:
            score -= 10
            ace_count -= 1

        return score

# SixDeck Class
class SixDeck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for _ in range(6):  # 6 decks
            for suit in ["Spades", "Clubs", "Hearts", "Diamonds"]:
                for val in range(1, 14):
                    self.cards.append(Card(val, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def length(self):
        return len(self.cards)

    def reset(self):
        self.cards = []
        self.build()

# AI Logic
def basic_strategy(player_hand, dealer_card):
    def calculate_score(hand):
        score = 0
        ace_count = 0
        for card in hand:
            if card.val == 1:
                ace_count += 1
                score += 11
            elif card.val >= 10:
                score += 10
            else:
                score += card.val
        while score > 21 and ace_count > 0:
            score -= 10
            ace_count -= 1
        return score

    player_score = calculate_score(player_hand)
    dealer_value = dealer_card.val

    if player_score >= 17:
        return "Stand", "Your hand is strong enough to avoid the risk of busting."
    elif 13 <= player_score <= 16:
        if dealer_value < 7:
            return "Stand", "The dealer is likely to bust with a weak card."
        else:
            return "Hit", "The dealer has a strong card, so you need to improve your hand."
    elif player_score == 12:
        if 4 <= dealer_value <= 6:
            return "Stand", "The dealer's weak card increases their chances of busting."
        else:
            return "Hit", "The dealer's strong card requires you to strengthen your hand."
    elif player_score == 11:
        if dealer_value < 11:
            return "Double Down", "You have the best chance to maximize your winnings."
        else:
            return "Hit", "The dealer's strong card makes doubling too risky."
    elif player_score == 10:
        if dealer_value < 10:
            return "Double Down", "The dealer's weaker card gives you an advantage."
        else:
            return "Hit", "The dealer's card is too strong to risk doubling."
    elif player_score == 9:
        if 3 <= dealer_value <= 6:
            return "Double Down", "The dealer's weak card increases your odds of success."
        else:
            return "Hit", "You need to improve your hand against the dealer's strong card."
    else:
        return "Hit", "Your hand is too weak to stand or double."

# Main Game Logic with GUI
def BlackJackGame():
    root = tk.Tk()
    root.title("BlackJack Game with AI Suggestions")

    dealer = Dealer()
    player = Player()
    deck = SixDeck()
    deck.shuffle()

    def deal():
        dealer.reset()
        player.reset()
        dealer.draw(deck)
        dealer.draw(deck)
        player.draw(deck)
        player.draw(deck)
        update_game_display()

    def update_game_display():
        dealer_display = f"{dealer.hand[0].val} of {dealer.hand[0].suit}, [Hidden]"
        player_display = ', '.join(f"{card.val} of {card.suit}" for card in player.hand)

        dealer_label.config(text=f"Dealer's Hand: {dealer_display}")
        player_label.config(text=f"Player's Hand: {player_display}")

        suggestion, reason = basic_strategy(player.hand, dealer.hand[0])
        suggestion_label.config(text=f"AI Suggestion: {suggestion}")
        reason_label.config(text=f"Reason: {reason}")

    # Labels and Buttons
    dealer_label = tk.Label(root, text="Dealer's Hand: ", font=("Arial", 14))
    dealer_label.pack()

    player_label = tk.Label(root, text="Player's Hand: ", font=("Arial", 14))
    player_label.pack()

    suggestion_label = tk.Label(root, text="AI Suggestion: None", font=("Arial", 12), fg="blue")
    suggestion_label.pack()

    reason_label = tk.Label(root, text="Reason: None", font=("Arial", 10), fg="green")
    reason_label.pack()

    tk.Button(root, text="Deal", command=deal, font=("Arial", 14), bg="lightblue").pack()

    root.mainloop()

BlackJackGame()
