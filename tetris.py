import pygame
import os
import sys

#COULEURS
blueBG = 80
maxk = 6
blueBGdir = 1 # pour le retour inverse du bleu vers sa valeur initiale
colorText = (255,255,255)
colorGrid = (20,20,30)

WIDTH = 450
HEIGHT = 600
MUSIC = "music.mp3"

L = 20 # nombre de lignes
C = 10 # nombre de colonnes (à priori on ne changera pas ce nombre)
LEVEL = 1 # difficulté
COLOR = [(255,0,0),(0,255,0),(0,0,255)] #couleurs des pièces

boardWidth = 6*WIDTH//10
boardHeight = boardWidth * L//C
slotSize = boardWidth//C
slotBorder = slotSize // 7

xBoard = (WIDTH - boardWidth)//2
yBoard = (HEIGHT - boardHeight)//2


class Tetris:
    """
    On définit le Tetris comme une matrice qui se fera actualiser au fil du temps.
    Les cases 0 sont vides.
    Pour n non nul, si self.board[i][j] = n, alors la case est pleine et est de couleur COLOR[n].
    """
    def __init__(self, width, length, level):
        self.width = width
        self.length = length
        self.level = level
        self.board = [[0]*width for i in range(length)] #matrice de taille L*C qui caractérise le plateau de jeu
        self.playing = None #pièce qu'on joue
        self.score = 0



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
game = Tetris(C, L, LEVEL)
pygame.display.set_caption("Tetris")

pygame.mixer.music.load(MUSIC)
pygame.mixer.music.play(loops=-1)

clock = pygame.time.Clock()

def drawSlot(screen, x, y, color):
    pygame.draw.rect(screen, color, (x,y,slotSize,slotSize))
    (r,g,b) = color
    contrast = 65
    if r<contrast:
        r = contrast
    if g<contrast:
        g = contrast
    if b <contrast:
        b = contrast
    colorb = (r-contrast,g-contrast, b-contrast)
    pygame.draw.rect(screen, colorb, (x,y,slotSize,slotBorder))
    pygame.draw.rect(screen, colorb, (x,y,slotBorder,slotSize))
    pygame.draw.rect(screen, colorb, (x+slotSize-slotBorder,y,slotBorder,slotSize))
    pygame.draw.rect(screen, colorb, (x,y+slotSize-slotBorder,slotSize,slotBorder))


def gameUpdate(screen, game):
    """
    Mise à jour en temps réel du jeu, fonction principale.
    """
    #On commence par mettre à jour le jeu
    # à compléter
    #Puis on dessine la matrice
    pygame.draw.rect(screen, colorGrid, (xBoard,yBoard,boardWidth,boardHeight))
    drawSlot(screen,0,0,(255,0,0))

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