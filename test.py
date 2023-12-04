import pygame
import sys
import random
from pygame import mixer

# Initialize Pygame
pygame.init()
pygame.font.init()

# Constants
WIDTH, HEIGHT = 1200, 739
CARD_WIDTH, CARD_HEIGHT = 100, 125 # 3/4 Card Ratio
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#Music/Sound
pygame.mixer.init()
pygame.mixer.music.load("sound/card.mp3")
mixer.music.set_volume(0.7)
# Game Icons
bg = pygame.image.load("images/table.jpeg")
help = pygame.image.load("images/help.png")
win_icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(win_icon)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

font = pygame.font.SysFont("Consolas Bold", 100)

suits = ["diamonds", "hearts", "spades", "clubs"]

def draw_card(card, x, y):
    card_img = card_images[card]["image"]

    # Get the original dimensions
    original_width, original_height = card_img.get_size()

    # Calculate the scale factor to fit within the specified CARD_WIDTH and CARD_HEIGHT
    scale_factor = min(CARD_WIDTH / original_width, CARD_HEIGHT / original_height)

    # Scale the card image while maintaining the aspect ratio
    card_img = pygame.transform.scale(card_img, (int(original_width * scale_factor), int(original_height * scale_factor)))

    screen.blit(card_img, (x, y))

def deal_card(remaining_cards):
    card = random.choice(remaining_cards)
    remaining_cards.remove(card)
    return card

def calculate_score(hand):
    score = 0
    num_aces = 0

    for card in hand:
        if isinstance(card["value"], int):
            score += card["value"]
        elif card["value"] in ["Jack", "Queen", "King"]:
            score += 10
        elif card["value"] == "Ace":
            num_aces += 1
            score += 11  # Assume Ace as 11 initially

    # Adjust for Aces
    while num_aces > 0 and score > 21:
        score -= 10  # Change the value of an Ace from 11 to 1
        num_aces -= 1

    return score

def dealer_logic(dealer_hand):
    pygame.time.wait(1000)
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(deal_card(remaining_cards))

def display_result(player_score, dealer_score):
    font = pygame.font.SysFont(None, 100)
    
    if player_score > 21:
        text = font.render("Bust!", True, RED)
    elif dealer_score > 21:
        text = font.render("Dealer Bust!", True, GREEN)
    elif player_score > dealer_score:
        text = font.render("You Win!", True, GREEN)
    elif dealer_score > player_score:
        text = font.render("You Lose!", True, RED)
    else:
        text = font.render("Tie!", True, WHITE)

    screen.blit(text, (300, 250))
    pygame.display.flip()
    pygame.time.delay(3000)

def load_card_images(suits):
    card_images = {}
    for i in range(1, 11):
        for suit in suits:
            card_images[f"{i}_of_{suit}"] = {"image": pygame.image.load(f'Cards/{i}_of_{suit}.png'), "suit": suit}

    face_cards = ['Jack', 'Queen', 'King']
    for face in face_cards:
        for suit in suits:
            card_images[f"{face}_of_{suit}"] = {"image": pygame.image.load(f'Cards/{face}_of_{suit}.png'), "suit": suit}

    return card_images

#MainLoop


while True:
    # Set the initial offset values
    card_offset_x = 500
    card_offset_y = 10
    

    def main():
        global card_images  # Declare card_images as a global variable
        card_images = load_card_images(suits)

        global remaining_cards
        remaining_cards = [{"value": i, "suit": suit} for i in range(1, 11) for suit in suits]

        player_hand = [deal_card(remaining_cards) for _ in range(2)]
        dealer_hand = [deal_card(remaining_cards) for _ in range(2)]  # Dealer starts with two cards
        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        player_hand.append(deal_card(remaining_cards))
                        pygame.mixer.music.play(1)
                        pygame.time.delay(1500)
                        if calculate_score(player_hand) > 21:
                            game_over = True

                    if event.key == pygame.K_d:
                        # Player stands, now let the dealer play
                        dealer_logic(dealer_hand)
                        game_over = True

            # Draw background
            screen.blit(bg, [0, 0])
            
            # Draw Help
            screen.blit(help,[0, 639])

            # Draw player's hand
            for i, card in enumerate(player_hand):
                draw_card(f'{card["value"]}_of_{card["suit"]}', i * CARD_WIDTH + card_offset_x, HEIGHT - CARD_HEIGHT * 2)

            # Draw dealer's hand
            for i, card in enumerate(dealer_hand):
                draw_card(f'{card["value"]}_of_{card["suit"]}', i * CARD_WIDTH + card_offset_x, CARD_HEIGHT + card_offset_y)
                
                
            # Display scores
            player_score_text = font.render(str(calculate_score(player_hand)), True, BLACK)
            dealer_score_text = font.render(str(calculate_score(dealer_hand)), True, BLACK)
            screen.blit(player_score_text, (570, 630))
            screen.blit(dealer_score_text, (570, 50))

            # Update the display
            pygame.display.flip()

            # Check for game over conditions
            player_score = calculate_score(player_hand)
            dealer_score = calculate_score(dealer_hand)

            if player_score == 21 or player_score > 21:
                game_over = True

            if dealer_score == 21 or dealer_score > 21:
                game_over = True

            # Cap the frame rate
            clock.tick(FPS)

        display_result(player_score, dealer_score)

    if __name__ == "__main__":
        main()
