import requests

import json

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import pygame

# Define the API endpoint for the deck of cards

deck_api_url = "https://deckofcardsapi.com/api/deck/new/shuffle/"

# Define the rank-value mapping for the cards

rank_values = {

    "ACE": 1,

    "2": 2,

    "3": 3,

    "4": 4,

    "5": 5,

    "6": 6,

    "7": 7,

    "8": 8,

    "9": 9,

    "10": 10,

    "JACK": 10,

    "QUEEN": 10,

    "KING": 10,

}

# Define the Card class

class Card:

    def __init__(self, rank, suit):

        self.rank = rank

        self.suit = suit

        self.value = rank_values[rank]

    def __str__(self):

        return f"{self.rank} of {self.suit}"

# Define the Deck class

class Deck:

    def __init__(self):

        self.cards = []

        self.num_decks = 1

        self.shuffle()

    def shuffle(self):

        deck_api_response = requests.get(deck_api_url + f"?deck_count={self.num_decks}")

        deck_api_data = json.loads(deck_api_response.text)

        deck_id = deck_api_data["deck_id"]

        draw_api_url = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={self.num_decks*52}"

        draw_api_response = requests.get(draw_api_url)

        draw_api_data = json.loads(draw_api_response.text)

        for card_data in draw_api_data["cards"]:

            card = Card(card_data["value"], card_data["suit"])

            self.cards.append(card)

    def deal(self):

        return self.cards.pop()

# Define the Hand class

class Hand:

    def __init__(self):

        self.cards = []

    def add_card(self, card):

        self.cards.append(card)

    def get_value(self):

        value = sum(card.value for card in self.cards)

        if "ACE" in [card.rank for card in self.cards] and value <= 11:

            value += 10

        return value

    def is_bust(self):

        return self.get_value() > 21

# Define the Player class

class Player:

    def __init__(self, name, balance):

        self.name = name

        self.balance = balance

        self.bet = 0

        self.hand = Hand()

    def place_bet(self):

        while True:

            try:

                bet = int(input("Enter your bet: "))

                if bet > self.balance:

                    print("You don't have enough balance.")

                elif bet <= 0:

                    print("Bet must be greater than zero.")

                else:

                    self.bet = bet

                    self.balance -= bet

                    break

            except ValueError:

                print("Invalid bet. Try again.")

    def win_bet(self):

        self.balance += 2*self.bet

    def lose_bet(self):

        self.bet = 0

# Define the Dealer class

class Dealer:

    def __init__(self):

        self.hand = Hand()

    def hit(self, deck):

        card = deck.deal()

        self.hand.add_card(card)

    def stand(self):

        pass

# Define the main function
def main():

# Initialize the game

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Blackjack")
# Initialize the deck and players

deck = Deck()

player = Player("Player 1", 1000)

dealer = Dealer()

# Start the game loop

while True:

    # Check for events

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            sys.exit()

    

    # Check if player has enough balance to play

    if player.balance <= 0:

        print("You don't have enough balance to play.")

        break

    

    # Place bet

    player.place_bet()

    print(f"Bet: {player.bet}")

    

    # Deal cards

    player.hand = Hand()

    dealer.hand = Hand()

    player.hand.add_card(deck.deal())

    dealer.hand.add_card(deck.deal())

    player.hand.add_card(deck.deal())

    dealer.hand.add_card(deck.deal())

    print("Player's hand:")

    print(*player.hand.cards, sep=", ")

    print(f"Total value: {player.hand.get_value()}")

    print("Dealer's hand:")

    print(dealer.hand.cards[0])

    

    # Player's turn

    while True:

        choice = input("Do you want to hit or stand? ").strip().lower()

        if choice == "hit":

            player.hand.add_card(deck.deal())

            print("Player's hand:")

            print(*player.hand.cards, sep=", ")

            print(f"Total value: {player.hand.get_value()}")

            if player.hand.is_bust():

                print("Bust! You lose.")

                player.lose_bet()

                break

        elif choice == "stand":

            break

        else:

            print("Invalid choice. Try again.")

    

    # Dealer's turn

    if not player.hand.is_bust():

        print("Dealer's hand:")

        print(*dealer.hand.cards, sep=", ")

        print(f"Total value: {dealer.hand.get_value()}")

        while dealer.hand.get_value() < 17:

            dealer.hit(deck)

            print("Dealer hits.")

            print(*dealer.hand.cards, sep=", ")

            print(f"Total value: {dealer.hand.get_value()}")

            if dealer.hand.is_bust():

                print("Dealer busts! You win.")

                player.win_bet()

                break

    

    # Determine the winner

    if not player.hand.is_bust() and not dealer.hand.is_bust():

        if player.hand.get_value() > dealer.hand.get_value():

            print("You win!")

            player.win_bet()

        elif player.hand.get_value() == dealer.hand.get_value():

            print("Push.")

            player.balance += player.bet

        else:

            print("You lose.")

            player.lose_bet()

    print(f"Balance: {player.balance}")

    

    # Ask player if they want to play again

    choice = input("Do you want to play again? ").strip().lower()

    if choice != "yes":

        break

pygame.quit()




