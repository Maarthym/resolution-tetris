import pygame
import os
import sys
import random
import math

#COULEURS
blueBG = 80
maxk = 6
blueBGdir = 1 # pour le retour inverse du bleu vers sa valeur initiale
colorText = (255,255,255)
colorGrid = (20,20,30)

WIDTH = 450
HEIGHT = 600
FPS = 60
MUSIC = "music.mp3"

L = 20 # nombre de lignes
C = 10 # nombre de colonnes (à priori on ne changera pas ce nombre)
LEVEL = 1 # difficulté
COLOR = [(255,0,0),(0,255,0),(0,0,255)] #couleurs des pièces

TYPE = [
    [[1,1,1,1]]
]

solG = [0.00196302, 1.60274096, 0.02719349] #résultats du script visu_vitesse cherchant à trouver une fonction qui rend compte de la vitesse des tetrominoes

def gravity(level):
    """
    1G correspond à un carré qui descend PAR image
    """
    return solG[0]*(solG[1])**level + solG[2]

def T(level):
    """
    Calcul de la période de descente d'une pièce.
    C'est le nombre de frames à attendre pour que la pièce tombe.
    On arrondi arbitrairement à l'entier supérieur.
    """
    G = gravity(level)
    return math.ceil(1/G)

boardWidth = 6*WIDTH//10
boardHeight = boardWidth * L//C
slotSize = boardWidth//C
slotBorder = slotSize // 7

xBoard = (WIDTH - boardWidth)//2
yBoard = (HEIGHT - boardHeight)//2 + 10

pygame.init()
font = pygame.font.Font(None, 36)

def drawSlot(screen, i, j, color):
    x = xBoard + i * slotSize
    y = yBoard + j * slotSize
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

def drawText(screen, x,y,t,c=(255,255,255)):
    text = font.render(t, True, c)
    screen.blit(text, (x, y))
def drawTextXCentered(screen, x,y,t,c=(255,255,255)):
    text = font.render(t, True, c)
    l,h = text.get_size()
    screen.blit(text, (x-l//2, y))

class Tetromino:
    """
    Un Tetromino est une pièce du jeu. Ici on les défini en tant qu'objet de par leur complexité : on va les bouger, les figer, les colorer, leur donner une forme parmi 7 disponibles (TYPE)...
    """
    def __init__(self, game, type, color, i, j):
        self.i = i
        self.j = j
        self.game = game
        self.type = type # matrice avec des 1 pour les pièces occupées et des 0 pour les pièces non-occupées
        self.color = color
        self.update()

    def testmove(self, mi, mj):
        """
        Vérifie au préalable si le mouvement peut-être fait
        """
        pass

    def move(self, mi, mj):
        for k in range(len(self.type)):
            for l in range(len(self.type[k])):
                if self.type[k][l] == 1:
                    self.game.board[self.i+k][self.j + l] = 0
        self.i = self.i + mi
        self.j = self.j + mj
        for k in range(len(self.type)):
            for l in range(len(self.type[k])):
                if self.type[k][l] == 1:
                    self.game.board[self.i+k][self.j + l] = 0

    def rotate(self):
        pass

    def down(self):
        self.move(0,-1) # il tombe

    def update(self):
        self.move(0,0) #ceci va simplement ajouter la pièce telle qu'elle est dans la matrice


class Tetris:
    """
    On définit le Tetris comme une matrice qui se fera actualiser au fil du temps.
    Les cases 0 sont vides.
    Pour n non nul, si self.board[i][j] = n, alors la case est pleine et est de couleur COLOR[n].
    """
    def __init__(self, width, length, level, screen):
        self.width = width
        self.length = length
        self.setLevel(level)
        self.board = [[-1]*width for i in range(length)] #matrice de taille L*C qui caractérise le plateau de jeu
        self.playing = None #pièce qu'on joue
        self.score = 0
        self.screen = screen
        self.frameclock = 0
        self.next = self.randomizeNext()
        self.spawn()

    def spawn(self):
        if self.playing != None:
            self.playing.update()
        tetroType = self.next.pop()
        nc = len(COLOR)
        col = random.randint(0,nc) # on modélise la couleur par un entier qui est son indice dans le tableau COLOR
        self.playing = Tetromino(self, tetroType, col, C//2, 0)

    def setLevel(self, level):
        self.level = level
        self.T = T(level)

    def incrClock(self):
        self.frameclock += 1
        if self.frameclock == self.T:
            self.frameclock = 0
            self.playing.down()


    def randomizeNext(self):
        l = TYPE.copy()
        random.shuffle(l)
        return l

    def update(self):
        drawTextXCentered(self.screen, WIDTH//2, 10, f"Score : {self.score}")
        self.incrClock()
        drawText(self.screen, 10, HEIGHT - 40, f"Lv.{self.level}")
        for i in range(L):
            for j in range(C):
                p = self.board[i][j]
                if p >= 0:
                    drawSlot(screen, i, j, COLOR[p])


screen = pygame.display.set_mode((WIDTH, HEIGHT))
game = Tetris(C, L, LEVEL, screen)
pygame.display.set_caption("Tetris")

pygame.mixer.music.load(MUSIC)
pygame.mixer.music.play(loops=-1)

clock = pygame.time.Clock()



def gameUpdate(screen, game):
    """
    Mise à jour en temps réel du jeu, fonction principale.
    """
    #On commence par mettre à jour le jeu
    # à compléter
    #Puis on dessine la matrice
    pygame.draw.rect(screen, colorGrid, (xBoard,yBoard,boardWidth,boardHeight))
    game.update()

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
    clock.tick(FPS)

pygame.mixer.music.stop()
pygame.quit()
sys.exit()