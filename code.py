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

# Player settings
player_width = 195
player_height = 109
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5
player_health = 3

# Paw settings
paw_width = 30
paw_height = 30
paw_speed = 7
paws = []

# Enemy settings
enemy_width = 100
enemy_height = 93
enemy_speed_slow = 2
enemy_speed_fast = 4
enemies = []
enemy_spawn_time = 2000
enemy_timer = 0

# Score
score = 0

def check_collision(rect1, rect2):
    return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))

# Game state
game_over = False

# Draw text function
def draw_text(text, size, color, surface, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# Restart game function
def restart_game():
    global player_x, player_y, paws, enemies, score, game_over, enemy_timer, player_health
    player_x = screen_width // 2 - player_width // 2
    player_y = screen_height - player_height - 10
    paws.clear()
    enemies.clear()
    player_health = 3
    score = 0
    game_over = False
    enemy_timer = 0
    pygame.mixer.music.play(-1)
# Main game loop
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

        if not game_over:
            # Handle player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
                player_x += player_speed
            # Update paw positions
            for paw in paws:
                paw[1] -= paw_speed
            paws = [paw for paw in paws if paw[1] > 0]

            # Update enemy positions and spawn new ones
            current_time = pygame.time.get_ticks()
            if current_time - enemy_timer > enemy_spawn_time:
                enemy_type = random.choice(['slow', 'fast'])
                enemy_x = random.randint(0, screen_width - enemy_width)
                enemy_y = -enemy_height
                enemies.append([enemy_x, enemy_y, enemy_type, 1])
                enemy_timer = current_time

            for enemy in enemies:
                if enemy[2] == 'slow':
                    enemy[1] += enemy_speed_slow
                else:
                    enemy[1] += enemy_speed_fast
            # Check for collisions between paws and enemies
            for paw in paws[:]:
                for enemy in enemies[:]:
                    if check_collision((paw[0], paw[1], paw_width, paw_height),
                                       (enemy[0], enemy[1], enemy_width, enemy_height)):
                        paws.remove(paw)
                        enemy[3] -= 1

                        if enemy[3] <= 0:
                            enemies.remove(enemy)
                            score += 1

                        break

            # Remove enemies that are off the screen or have been destroyed
            enemies = [enemy for enemy in enemies if enemy[1] < screen_height]

            # Check for collisions between player and enemies
            for enemy in enemies[:]:
                if check_collision((player_x, player_y, player_width, player_height),
                                   (enemy[0], enemy[1], enemy_width, enemy_height)):
                    player_health -= 1
                    enemies.remove(enemy)
                    if player_health <= 0:
                        game_over = True
                    break
        # Clear the screen and draw everything
        screen.blit(background_image, (0, 0))

        # Draw the player
        screen.blit(player_image, (player_x, player_y))

        # Draw the paws
        for paw in paws:
            screen.blit(paw_image, (paw[0], paw[1]))

        # Draw the enemies with their respective images based on type
        for enemy in enemies:
            if enemy[2] == 'slow':
                screen.blit(enemy_image1, (enemy[0], enemy[1]))
            else:
                screen.blit(enemy_image2, (enemy[0], enemy[1]))

        # Draw score and health on the screen
        draw_text(f'Score: {score}', 30, (255, 255, 255), screen, 10, 10)
        draw_text(f'Health: {player_health}', 30, (255, 255, 255), screen, 10, 50)

    else:
    pygame.mixer.music.stop()
    screen.fill((0, 0, 0))
    draw_text('Game over', 60, (255, 0, 0), screen, screen_width // 2 - 150, screen_height // 2 - 30)
    draw_text('(Нажмите R для перезапуска)', 30, (255, 255, 255), screen, screen_width // 2 - 160,
                  screen_height // 2 + 20)

        # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)