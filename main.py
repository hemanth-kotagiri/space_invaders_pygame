import pygame
import random
import math
from pygame import mixer
import os
import platform

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Alien Invasion")

# Player details
playerX, playerY = 390, 490
logo = pygame.image.load("spaceship_logo.png")
player = pygame.image.load("player.png")

# Enemy details
no_of_enemies = 6
enemy = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
for i in range(no_of_enemies):
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemy.append(pygame.image.load("enemy.png"))
    pygame.display.set_icon(logo)
    # Change in enemy pos
    enemyXChange.append(2)
    enemyYChange.append(40)

# Change in player pos
playerXChange = 0
playerYChange = 0

# background image
background = pygame.image.load('background.jpg')

# Background music
if platform.system() == "Linux":
    music_file_name = "bgm.ogg"
else:
    music_file_name = "bgm.mp3"

mixer.music.load(music_file_name)
mixer.music.play(-1)


# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 490
bulletYChange = 10
bullet_state = 'ready'

# Score
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
fontX = 10
fontY = 10


def showScore(x, y):
    score = font.render("Score : "+str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game over
gameOverFont = pygame.font.Font('freesansbold.ttf', 64)
totalScore = pygame.font.Font('freesansbold.ttf', 32)


def game_over_text():
    text = gameOverFont.render("GAME OVER", True, (255, 255, 255))
    total = totalScore.render(
        "TOTAL SCORE : "+str(score_val), True, (255, 255, 255))
    screen.blit(text, (200, 250))
    screen.blit(total, (270, 330))


def fireBullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x+16, y+10))


def drawPlayer(xPos, yPos):
    screen.blit(player, (xPos, yPos))


def drawEnemy(xPos, yPos, i):
    screen.blit(enemy[1], (xPos, yPos))


def checkCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(bulletX-enemyX, 2) +
                         math.pow(bulletY-enemyY, 2))
    if distance < 27:
        return True
    return False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange = -5
            if event.key == pygame.K_RIGHT:
                playerXChange = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletSound = mixer.Sound('laser.wav')
                    bulletSound.play()
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0

    playerX += playerXChange

    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(no_of_enemies):
        if enemyY[i] > 440:
            # Game over condition
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyXChange[i]
        if enemyX[i] < 0:
            enemyXChange[i] = 2
            enemyY[i] += enemyYChange[i]
        elif enemyX[i] >= 736:
            enemyXChange[i] -= 2
            enemyY[i] += enemyYChange[i]
        # Checking for collision
        collision = checkCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_val += 1
            enemyX[i], enemyY[i] = random.randint(
                0, 735), random.randint(50, 150)

        drawEnemy(enemyX[i], enemyY[i], i)
        showScore(fontX, fontY)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYChange

    drawPlayer(playerX, playerY)
    pygame.display.update()
