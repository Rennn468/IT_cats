import pygame
import sys
import random

pygame.init()

# Set up the game window
screen_width = 800
screen_height = 602
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game")

# Set the frame rate
clock = pygame.time.Clock()

try:
    player_image = pygame.image.load("player.png")
    paw_image = pygame.image.load("paw.png")
    enemy_image1 = pygame.image.load("enemy1.png")  # Slow enemy
    enemy_image2 = pygame.image.load("enemy2.png")  # Fast enemy
    background_image = pygame.image.load("background.png")
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()

# load music
pygame.mixer.music.load('music.mp3')
# Setting the volume ( 0.0 - 1.0)
pygame.mixer.music.set_volume(0.5)

# Start music
pygame.mixer.music.play(-1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                # Create a paw at the current player position
                paw_x = player_x + player_width // 2 - paw_width // 2
                paw_y = player_y
                paws.append([paw_x, paw_y])

            if event.key == pygame.K_r and game_over:
                restart_game()

        # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)