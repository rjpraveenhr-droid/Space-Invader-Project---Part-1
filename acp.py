
import math
import random
import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

PLAYER_START_X = 370
PLAYER_START_Y = 380

ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 150

COLLISION_DISTANCE = 27
NUM_OF_ENEMIES = 6

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invader")

# Images
background = pygame.image.load('background.png')
background = pygame.transform.scale(
    background, (SCREEN_WIDTH, SCREEN_HEIGHT)
)

icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('player.png')
enemyImg = pygame.image.load('enemy.png')
bulletImg = pygame.image.load('bullet.png')

# Player
playerX = PLAYER_START_X
playerY = PLAYER_START_Y
playerX_change = 0

# Player speed
player_speed = 5

# Lives
lives = 3

# Bullet
bulletX = 0
bulletY = PLAYER_START_Y
bullet_speed = 10
bullet_state = "ready"

# Enemies
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

enemy_speed = 4
enemy_down_speed = 40

for i in range(NUM_OF_ENEMIES):
    enemyX.append(random.randint(0, SCREEN_WIDTH - 64))
    enemyY.append(random.randint(
        ENEMY_START_Y_MIN, ENEMY_START_Y_MAX
    ))
    enemyX_change.append(enemy_speed)
    enemyY_change.append(enemy_down_speed)

# Score and Level
score_value = 0
level = 1

# Fonts
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
level_font = pygame.font.Font('freesansbold.ttf', 40)

# Level up message timer
level_up_time = 0

# Clock
clock = pygame.time.Clock()

# Functions

def show_score(x, y):
    score = font.render(
        "Score : " + str(score_value),
        True, (255, 255, 255)
    )
    screen.blit(score, (x, y))


def show_level():
    level_text = font.render(
        "Level : " + str(level),
        True, (255, 255, 255)
    )
    screen.blit(level_text, (620, 10))


def show_lives():
    small_rocket = pygame.transform.scale(
        playerImg, (28, 28)
    )

    for i in range(lives):
        screen.blit(small_rocket, (10 + i * 35, 55))
    global level_up_time
    
def level_up_message():
    if pygame.time.get_ticks() - level_up_time < 1500:
        message = level_font.render(
            "LEVEL UP! LEVEL " + str(level),
            True, (255, 255, 0)
        )
        screen.blit(message, (200, 200))


def game_over_text():
    over_text = over_font.render(
        "GAME OVER", True, (255, 255, 255)
    )
    screen.blit(over_text, (200, 220))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state

    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(
        (enemyX - bulletX) ** 2 +
        (enemyY - bulletY) ** 2
    )
    return distance < COLLISION_DISTANCE


def reset_enemy(i):
    enemyX[i] = random.randint(0, SCREEN_WIDTH - 64)
    enemyY[i] = random.randint(
        ENEMY_START_Y_MIN, ENEMY_START_Y_MAX
    )


def increase_level():
    global level
    global player_speed
    global enemy_speed
    global bullet_speed
    global level_up_time

    level += 1

    # Increase all speeds
    player_speed += 0.7
    enemy_speed += 0.8
    bullet_speed += 1.5

    # Update enemy speeds
    for i in range(NUM_OF_ENEMIES):
        if enemyX_change[i] > 0:
            enemyX_change[i] = enemy_speed
        else:
            enemyX_change[i] = -enemy_speed

    level_up_time = pygame.time.get_ticks()


# Game loop
running = True
game_over = False

while running:

    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if not game_over:

            if event.type == pygame.KEYDOWN:

                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    playerX_change = -player_speed

                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    playerX_change = player_speed

                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        bulletY = playerY
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key in [
                    pygame.K_LEFT, pygame.K_RIGHT,
                    pygame.K_a, pygame.K_d
                ]:
                    playerX_change = 0

    if not game_over:

        # Player movement
        playerX += playerX_change

        playerX = max(
            0, min(playerX, SCREEN_WIDTH - 64)
        )

        # Enemy movement
        for i in range(NUM_OF_ENEMIES):

            enemyX[i] += enemyX_change[i]

            # Enemy reaches screen edge
            if enemyX[i] <= 0 or enemyX[i] >= SCREEN_WIDTH - 64:

                enemyX_change[i] *= -1
                enemyY[i] += enemy_down_speed

            # Enemy reaches player area
            if enemyY[i] > 340:

                lives -= 1
                reset_enemy(i)

                if lives <= 0:
                    game_over = True
                    break

            # Draw enemy
            enemy(enemyX[i], enemyY[i], i)

        # Bullet movement
        if bullet_state == "fire":

            bulletY -= bullet_speed

            screen.blit(
                bulletImg, (bulletX + 16, bulletY)
            )

            if bulletY <= 0:
                bulletY = PLAYER_START_Y
                bullet_state = "ready"

        # Collision detection
        if bullet_state == "fire":

            for i in range(NUM_OF_ENEMIES):

                if isCollision(
                    enemyX[i], enemyY[i],
                    bulletX, bulletY
                ):

                    bulletY = PLAYER_START_Y
                    bullet_state = "ready"

                    score_value += 1

                    reset_enemy(i)

                    # Level increases every 5 points
                    if score_value % 5 == 0:
                        increase_level()

                    break

        # Draw player
        player(playerX, playerY)

        # Display score, level and lives
        show_score(10, 10)
        show_level()
        show_lives()

        # Display level up message
        level_up_message()

    else:
        game_over_text()
        show_score(10, 10)
        show_level()
        show_lives()

    pygame.display.update()

    clock.tick(60)

pygame.quit()
