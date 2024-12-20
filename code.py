import pygame
import sys
from random import randint


pygame.init()

# Set up the game window
screen_width = 800
screen_height = 602
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game")





# Set the frame rate
clock = pygame.time.Clock()

# Load images
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

class Player:
    def __init__(self):
        self.player_width = 195
        self.player_height = 109
        # self.player_x = screen_width // 2 - player_width // 2
        # self.player_y = screen_height - player_height - 10
        self.player_speed = 5
        self.player_health = 3
        self.rect = pygame.Rect(
            screen_width // 2 - self.player_width // 2,
            screen_height - self.player_height - 10,
            self.player_width,
            self.player_height
        )
    def update (self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.rect.x < screen_width - self.player_width:
            self.rect.x += self.player_speed

        # shooting
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            paws.append(Paw())

    def draw(self):
        screen.blit(player_image, (self.rect.x, self.rect.y))


player = Player()


class Paw:
    def __init__(self):
        self.paw_width = 30
        self.paw_height = 30
        self.paw_speed = 7
        self.rect = pygame.Rect(
            player.rect.centerx,
            player.rect.top,
            self.paw_width,
            self.paw_height
        )
    def update(self):
        self.rect.y -= self.paw_speed
    def draw(self):
        screen.blit(paw_image, (self.rect.x, self.rect.y))

paws = []


class Enemy:
    def __init__(self):
        self.enemy_width = 100
        self.enemy_height = 93
        self.enemy_speed = randint(4,8)
        self.enemy_spawn_time = 2000
        self.enemy_timer = 0
        self.rect = pygame.Rect(
            randint(0,800),
            0,
            self.enemy_width,
            self.enemy_height
        )
    def update(self):
        self.rect.y += self.enemy_speed

    def draw(self):
        if self.enemy_speed < 6:
            screen.blit(enemy_image1, (self.rect.x, self.rect.y))
        elif self.enemy_speed > 5:
            screen.blit(enemy_image2, (self.rect.x, self.rect.y))

    def lost(self):
        if self.rect.y >= screen_height:
            player.player_health -= 1




enemy = Enemy()






# Draw text function
def draw_text(text, size, color, surface, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

tick = 200
score = 0
player_health = 3
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    screen.blit(background_image, (0, 0))

    if player_health == 0:
        pygame.quit()

    tick -= 1
    if tick <= 0:
        enemy = Enemy()
        tick = 200

    player.update()
    player.draw()

    for paw in paws:
        if paw.rect.y < 0:  # delete off-screen paws
            paws.remove(paw)
        else:
            paw.update()
            paw.draw()


    enemy.update()
    enemy.draw()
    enemy.lost()



    # Draw score and health on the screen
    draw_text(f'Score: {score}', 30, (255, 255, 255), screen, 10, 10)
    draw_text(f'Health: {player_health}', 30, (255, 255, 255), screen, 10, 50)
    # else:
    #    pygame.mixer.music.stop()
    #    screen.fill((0, 0, 0))
    #    draw_text('Game over', 60, (255, 0, 0), screen, screen_width // 2 - 150, screen_height // 2 - 30)
    #    draw_text('(Нажмите R для перезапуска)', 30, (255, 255, 255), screen, screen_width // 2 - 160, screen_height // 2 + 20)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)