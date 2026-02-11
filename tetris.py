import pygame
import os
import sys

#COULEURS
blueBG = 80
maxk = 6
blueBGdir = 1 # pour le retour inverse du bleu vers sa valeur initiale
colorText = (255,255,255)
colorGrid = (20,20,30)

WIDTH = 500
LENGTH = 500
MUSIC = "music.mp3"

class Tetris:
    def __init__(self):
        pass

pygame.init()
screen = pygame.display.set_mode((WIDTH, LENGTH))
game = Tetris()
pygame.display.set_caption("Tetris")

pygame.mixer.music.load(MUSIC)
pygame.mixer.music.play(loops=-1)

clock = pygame.time.Clock()

def gameUpdate(screen, game):
    """
    Mise à jour en temps réel du jeu, fonction principale.
    """

def bgChange(k):
    if k < maxk:
        return
    global blueBG, blueBGdir
    blueBG += blueBGdir
    if blueBG == 100:
        blueBGdir = -1
    if blueBG == 80:
        blueBGdir = 1

running = True
k = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    k += 1
    bgChange(k)
    if k == maxk:
        k = 0
    screen.fill((45,45,blueBG))

    gameUpdate(screen, game)

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()
sys.exit()