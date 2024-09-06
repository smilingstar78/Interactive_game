import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Word Guessing Game")

# Load images
background = pygame.image.load('background6.jpg')  # Use your chosen background image
background = pygame.transform.scale(background, screen.get_size())  # Resize background to match screen size
hangman_images = [pygame.image.load(f'hangman_stage_{i}.png') for i in range(8)]

# List of words
words = ["hello", "cat", "dogs", "butterfly", "world", "abdullah", "psychology"]

# Choose a random word
random_word = random.choice(words)
display = "_" * len(random_word)
attempts = 7

# Font for rendering text
font = pygame.font.Font(None, 74)  # Font for the word
small_font = pygame.font.Font(None, 36)  # Font for the attempts left
congrats_font = pygame.font.Font(None, 30)  # Smaller font for the congratulations message
game_over_font = pygame.font.Font(None, 24)  # Even smaller font for the game over message

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
box_color = (0, 0, 0, 0)  # Transparent background for the box
border_color = black  # Black for the box border

# Box settings
box_width = 60
box_height = 60
box_margin = 10

def display_message(message, color, font):
    # Display a message on the game screen
    screen.blit(background, (0, 0))  # Clear the screen with the background
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Close on ESC key
                    pygame.quit()
                    return

# Game loop
running = True
while running and attempts > 0 and "_" in display:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            guess = pygame.key.name(event.key).lower()

            if guess in random_word:
                display = "".join(
                    guess if random_word[i] == guess else display[i]
                    for i in range(len(random_word))
                )
            else:
                attempts -= 1

    # Get updated screen size and resize background accordingly
    screen_size = screen.get_size()
    background = pygame.transform.scale(pygame.image.load('background6.jpg'), screen_size)

    # Clear screen and draw background
    screen.blit(background, (0, 0))

    # Draw the boxes around each letter or underscore
    for i in range(len(display)):
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)  # Create a surface with alpha channel
        box_surface.fill(box_color)  # Fill with transparent color
        pygame.draw.rect(box_surface, border_color, (0, 0, box_width, box_height), 3)  # Draw black border with width 3

        box_rect = pygame.Rect(
            (screen.get_width() // 2 - (box_width * len(display)) // 2) + (box_width + box_margin) * i,
            screen.get_height() // 2 - box_height // 2,
            box_width,
            box_height
        )
        screen.blit(box_surface, box_rect)  # Blit the transparent box onto the main screen

        # Draw the letter or underscore inside the box
        text = font.render(display[i], True, black)  # Render text in black to stand out against the transparent background
        text_rect = text.get_rect(center=box_rect.center)
        screen.blit(text, text_rect)

    # Draw hangman image in the corner
    hangman_image = hangman_images[6 - attempts]
    screen.blit(hangman_image, (10, 10))  # Position in the top-left corner

    # Draw attempts left
    attempts_text = small_font.render(f"Attempts left: {attempts}", True, white)
    screen.blit(attempts_text, (10, 500))

    pygame.display.flip()

if "_" not in display:
    # Display congratulations message
    display_message(f"Congratulations! You guessed the word: {random_word}", black, congrats_font)

if attempts == 0:
    # Display game over message
    display_message(f"Sorry, you ran out of attempts. The word was: {random_word}", red, game_over_font)

pygame.quit()
