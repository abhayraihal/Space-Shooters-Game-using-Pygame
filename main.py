import math
import pygame
import random
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen (inside the tuple, we have width, height of screen)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('space.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Shooters")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(20, 70))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet
# ready- can't see on screen, fire- bullet is in motion
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('Winter Christmas.otf', 50)
textX = 10
textY = 10

# Game over text
font_over = pygame.font.Font('Winter Christmas.otf', 100)


def show_score(x, y):
    score = font.render("Score : {}".format(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = font_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, p):
    screen.blit(enemyImg[p], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y - 20))


def is_collision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    if distance <= 27:
        return True
    return False


# Game Loop
running = True
while running:
    # RGB (0-255)
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if key is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = - 3
            if event.key == pygame.K_RIGHT:
                playerX_change = + 3
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_Sound = mixer.Sound('laser.wav')
                bullet_Sound.play()
                bulletX = playerX
                fire_bullet(bulletX, playerY)
        # if key is released then check
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking boundaries
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = 2
        elif enemyX[i] >= 736:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = - 2

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(20, 70)

        enemy(enemyX[i], enemyY[i], i)

    # bullet
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    player(playerX, playerY)

    show_score(textX, textY)
    # update screen
    pygame.display.update()
