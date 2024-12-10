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