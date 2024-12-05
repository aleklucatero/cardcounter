import random

# Constants
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
CARD_VALUES = {rank: min(index + 2, 10) if rank != 'A' else 11 for index, rank in enumerate(RANKS)}
CARD_VALUES['A'] = 11  # Ace initially counted as 11
HI_LO_VALUES = {rank: +1 if rank in ['2', '3', '4', '5', '6'] else -1 if rank in ['10', 'J', 'Q', 'K', 'A'] else 0 for rank in RANKS}

# Helper Functions
def create_deck(num_decks=1):
    """Creates a deck of 52 cards per number of decks."""
    return [(rank, suit) for suit in SUITS for rank in RANKS] * num_decks

def shuffle_deck(deck):
    """Shuffles the deck of cards."""
    random.shuffle(deck)

def calculate_score(hand):
    """Calculates the score of a hand."""
    score = sum(CARD_VALUES[rank] for rank, suit in hand)
    # Adjust for Aces if score > 21
    aces = sum(1 for rank, suit in hand if rank == 'A')
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1
    return score

def display_hand(hand, player_name="Player", hide_first_card=False):
    """Displays the hand of a player. Optionally hides the first card."""
    if hide_first_card:
        visible_hand = ['[Hidden Card]'] + [f"{rank} of {suit}" for rank, suit in hand[1:]]
        cards = ', '.join(visible_hand)
    else:
        cards = ', '.join(f"{rank} of {suit}" for rank, suit in hand)
    print(f"{player_name}'s Hand: {cards}")

def update_running_count(hand, running_count):
    """Updates the running count based on the Hi-Lo system."""
    for rank, suit in hand:
        running_count += HI_LO_VALUES[rank]
    return running_count

# Game Logic
def play_blackjack(num_decks=1):
    """Simulates a continuous blackjack game with Hi-Lo card counting."""
    # Set up
    deck = create_deck(num_decks)
    shuffle_deck(deck)
    running_count = 0
    decks_remaining = num_decks

    while True:
        if len(deck) < 10:  # Shuffle if too few cards remain
            print("\nReshuffling deck...")
            deck = create_deck(num_decks)
            shuffle_deck(deck)
            running_count = 0  # Reset running count after reshuffle
            decks_remaining = num_decks
        
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        
        # Update running count
        running_count = update_running_count(player_hand + dealer_hand, running_count)
        
        # Display initial hands
        display_hand(player_hand, "Player")
        print(f"Player's Score: {calculate_score(player_hand)}")
        display_hand(dealer_hand, "Dealer", hide_first_card=True)
        print(f"Running Count: {running_count}")
        print(f"True Count: {running_count / decks_remaining:.2f}")
        print()
        
        # Player's turn
        while True:
            score = calculate_score(player_hand)
            if score > 21:
                print("Player busts! Dealer wins.")
                break
            
            move = input("Choose an action: (h)it or (s)tand: ").lower()
            if move == 'h':
                card = deck.pop()
                player_hand.append(card)
                running_count = update_running_count([card], running_count)
                display_hand(player_hand, "Player")
                print(f"Player's Score: {calculate_score(player_hand)}")
                print(f"Running Count: {running_count}")
                print(f"True Count: {running_count / decks_remaining:.2f}")
            elif move == 's':
                break
        
        # Dealer's turn
        if calculate_score(player_hand) <= 21:
            print("\nDealer's Turn:")
            display_hand(dealer_hand, "Dealer")
            while calculate_score(dealer_hand) < 17:
                card = deck.pop()
                dealer_hand.append(card)
                running_count = update_running_count([card], running_count)
                display_hand(dealer_hand, "Dealer")

            dealer_score = calculate_score(dealer_hand)
            print(f"Dealer's Score: {dealer_score}")
            print(f"Final Running Count: {running_count}")
            print(f"Final True Count: {running_count / decks_remaining:.2f}")
            
            # Determine winner
            player_score = calculate_score(player_hand)
            if dealer_score > 21 or player_score > dealer_score:
                print("Player wins!")
            elif player_score < dealer_score:
                print("Dealer wins!")
            else:
                print("It's a tie!")

        # Ask if the player wants to play another round
        print("\n--- End of Round ---")
        play_again = input("Play another round? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

# Run the game
if __name__ == "__main__":
    play_blackjack(num_decks=6)
