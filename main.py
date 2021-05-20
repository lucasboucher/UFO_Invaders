import pygame
import random
from math import *
from pygame import mixer
import pickle
import time
       
#Initialise le jeu
pygame.init()

#Affiche l'ecran avec les dimensions : X = 800 | Y = 600
screen = pygame.display.set_mode((1000,400))

#background
background = pygame.image.load('image/Background-Shump.jpg')

#background sound
mixer.music.load('glorious_morning.mp3 ')
mixer.music.play(-1)
    
# Changer le titre de la fenetre
pygame.display.set_caption("UFO Invaders")

#Changer l'icone de la fenetre
icon = pygame.image.load('image/icon.png')
pygame.display.set_icon(icon)


#----------Joueur----------
player_sprite = pygame.image.load('image/plane_player.png')
playerX = 50
playerY = 90
playerX_change = 0
playerY_change = 0

#balle du joueur 
bulletplayer = pygame.image.load('image/bullet_player.png')
bulletX = playerX
bulletY = playerY
bulletX_change = 0.6*3

#----------UFO----------

ufo_num = 3 #Nombre d'ennemis au debut
ufoY = []
ufo_sprite = []
ufoX = []
ufoX_change = []

for i in range(ufo_num):
    ufoY.append(random.randint(0, 250))
    ufoX.append(random.randint(900, 1000))
    ufo_sprite.append(pygame.image.load('image/ufo.png'))


#La boucle du jeu
running = True

#--------Le score de la partie--------
score_value = 0
font = pygame.font.Font('image/pixelmix.ttf', 12) #La police d'ecriture du score et sa taille

def show_score(x, y):
    """Affiche le score sur l'ecran"""
    score = font.render("Score : {}".format(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

#Les tires de la balle 
bullet_state = "ready"
def New_Bullet_Player(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletplayer, (x+70, y+30))

def anim_boss(x, y, time):
    """ Animation du boss """

    #A chaque fois que la variable time avance de 1, l'animation continue
    boss_sprite = pygame.image.load(f'image/alien_boss_{time%24 + 1}.png')

    #Depose le sprite du boss sur l'ecran
    screen.blit(boss_sprite, (x, y))

def isCollision(enemyX, enemyY, bulletX, bulletY, taille_collision):
    """Check s'il y a une collision entre le tir et l'ennemi"""

    #Calcul de la distance entre la balle et l'ennemi
    distance = sqrt((pow(enemyX - bulletX, 2))+ (pow(enemyY - bulletY, 2)))

    #Si la distance est inferieure a "taille_collision" pixels, on a collision
    if distance < taille_collision:
        return True
    else:
        return False

#Le GAME OVER
def game_over_text():
    """Texte du Game Over"""
    font2 = pygame.font.Font('image/pixelmix.ttf', 150) #La police d'ecriture du GAME OVER et sa taille
    over_text = font2.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (10, 100))

#Variable qui va controler l'animation du boss
timer = 0

#Variable qui determine si on a perdu ou pas
game_over = False

#Variable qui determine si on a gagne
win = False

#Facteur d'acceleration, une fois que le boss arrive il devient effective
accel = 1

#Variables du boss
bulletboss = pygame.image.load('image/bullet_player.png')
bossX = 1000
bossY = 5
bullet_bossX = bossX
bullet_bossY = bossY
bullet_bossX_change = 0.2*9
boss_life = 13


while running == True :

    #----------------------- Gestions des autres parametres -----------------------
    #On fait progresser l'animation du boss, plus c'est eleve, plus l'animation est rapide
    timer += 0.25

    #Background
    screen.blit(background, (0, 0))

    #Montre le score en haut a gauche de l'ecran
    show_score(10,10)


    #----------------------- Gestion de l'ennemi -----------------------
    #Plus le score du joueur est eleve, plus on a d'ennemis
    if score_value % 15 == 0:
        score_value += 1
        ufo_num += 1
        ufoY.append(random.randint(0, 250))
        ufoX.append(random.randint(900, 1000))
        ufo_sprite.append(pygame.image.load('image/ufo.png'))

    #Faire apparaitre les ennemis
    for i in range(ufo_num-1):
        screen.blit(ufo_sprite[i],(ufoX[i],ufoY[i]))
        ufoX[i] -= 0.3 * accel

        #Si l'ennemi arrive a l'extremite gauche de l'ecran, on le fait respawn
        if -150 < ufoX[i] < 0 :
            ufoX[i] = random.randint(900, 1000)
            ufoY[i] = random.randint(0, 250)

            score_value -= 5

        #La hitbox de l'ennemi
        collision_ufo = isCollision(ufoX[i], ufoY[i], bulletX, bulletY, 27)
        if collision_ufo == True :

            #Reinitialise la balle
            bulletY = 7000
            bullet_state = "ready"

            #Ajoute 1 au score
            score_value += 1 

            #Joue un son lors de la collision
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()

            #Reinitialise la position de l'ennemi
            ufoX[i] = random.randint(900, 1000)
            ufoY[i] = random.randint(0, 250)

        #Collision avec le joueur
        collision_player_ufo = isCollision(playerX, playerY, ufoX[i], ufoY[i], 50)
        if collision_player_ufo == True:

            game_over = True
            ufoX[i] = -7000

            #Joue un son lors de la collision
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
    



    #------------------------ Gestion du boss ------------------------
    #Le boss apparait a partir de 50 points de score
    if score_value >= 50 :

        accel = 3

        #Position du boss
        anim_boss(bossX, bossY, ceil(timer))

        #Deplacement du boss
        bossX -= 0.05 * accel

        #Collision entre le boss et le joueur
        #La hitbox de l'ennemi
        collision_boss = isCollision(bossX+100, bossY+100, playerX, playerY, 100)
        if collision_boss == True :

            game_over = True
            bossX = -7000

            #Joue un son lors de la collision
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()

        #Collosion entre les tirs du boss et le joueur

        
        #La sante du boss
        if boss_life == 0 :
            win = True
            break

        
        
    


    #------------------------ Gestion du joueur ------------------------

    #Evenement qui permet de coder la croix pour fermer la fenetre
    for event in pygame.event.get():
        
        #Si on souhaite fermer le jeu
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #Lorsqu'on appuie sur une touche
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 1 
            if event.key == pygame.K_LEFT: 
                playerX_change = -1
            if event.key == pygame.K_DOWN: 
                playerY_change = 1
            if event.key == pygame.K_UP: 
                playerY_change = -1
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                bulletY = playerY
                bulletX = playerX
                New_Bullet_Player(bulletX,bulletY)
        
        # Lorsqu'on relache la touche
        if event.type == pygame.KEYUP:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    playerX_change = 0
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP:
                    playerY_change = 0
                if event.key == pygame.K_DOWN:
                    playerY_change = 0

    #Deplacement du joueur
    screen.blit(player_sprite,(playerX,playerY))
    playerX += 1*playerX_change * accel
    playerY += 1*playerY_change * accel

    # Limite des bordures
    if playerX >= 900:
        playerX = 899
    if playerY >= 250:
        playerY = 249
    if playerX <= 0:
        playerX = 1
    if playerY <= 0:
        playerY = 1

    

    #-------- Gestion des tirs du personnage --------

    #Mouvement du tir
    if bulletX >= 1000:
        #Les limites des tir, pour permettre au joueur de retirer
        bulletX = playerX
        bulletY = playerY
        bullet_state = "ready"

    if bullet_state is "fire":
        #Tant que la balle du joueur se trouve sur l'ecran, on ne peut pas encore tirer
        New_Bullet_Player(bulletX, bulletY)
        bulletX += bulletX_change * 2 * accel

    

    pygame.display.update() #Update l'ecran

    if score_value < 0:
        game_over = True 
        break

    #Si on a perdu le jeu
    if game_over :
        break

    


if game_over :
    #Boucle qui tourne tant qu'on ne quitte pas le jeu apres avoir perdu
    while game_over :

        #Background
        screen.blit(background, (0, 0))

        #Montre le score en haut a gauche de l'ecran
        show_score(10,10)

        #Evenement qui permet de coder la croix pour fermer la fenetre
        for event in pygame.event.get():

            #Si on souhaite fermer le jeu
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        #Affiche le message de game over
        game_over_text()

        pygame.display.update() #Update l'ecran
