import pygame
import os
import sys
import random
import math

pygame.init()

#COULEURS
blueBG = 80
maxk = 6
blueBGdir = 1 # pour le retour inverse du bleu vers sa valeur initiale
colorText = (255,255,255)
colorGrid = (20,20,30)

info = pygame.display.Info()
maxw = info.current_w
maxh = info.current_h
WIDTH = math.floor(0.25*maxw)
HEIGHT = 600/450*WIDTH
FPS = 60
MUSIC = "music.mp3"

L = 20 # nombre de lignes
C = 10 # nombre de colonnes (à priori on ne changera pas ce nombre)
LEVEL = 1 # difficulté
COLOR = [(random.randint(100,255), random.randint(100,255),random.randint(100,255)) for _ in range(15)] #couleurs des pièces

TYPE = [[
    [1,1],
    [0,1],
    [0,1]
    ],[
    [0,1],
    [0,1],
    [1,1]
    ],[
    [1],
    [1],
    [1],
    [1]
    ],[
    [1,0],
    [1,1],
    [0,1]
    ],[
    [0,1],
    [1,1],
    [1,0]
    ],[
    [1,1],
    [1,1],
    ],[
    [1,0],
    [1,1],
    [1,0]
    ]
]

solG = [0.00196302, 1.60274096, 0.02719349] #résultats du script visu_vitesse cherchant à trouver une fonction qui rend compte de la vitesse des tetrominoes

devmode = True

def gravity(level):
    """
    1G correspond à un carré qui descend PAR image
    """
    add = 0
    if devmode:
        add = 0
    return solG[0]*(solG[1])**level + solG[2] + add

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

font = pygame.font.Font(None, 36)

def drawSlot(screen, posx, posy, color):
    x = xBoard + posx * slotSize # j -> column -> x-axis
    y = yBoard + posy * slotSize # i -> line -> y-axis
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
    def __init__(self, game, type, color, x, y):
        self.x = x
        self.y = y
        self.game = game
        self.type = type # matrice avec des 1 pour les pièces occupées et des 0 pour les pièces non-occupées
        self.color = color
        self.isPlaying = True

    def testmove(self, mx, my):
        """
        Vérifie au préalable si le mouvement peut-être fait.
        """
        board = [[self.game.board[i][j] for j in range(self.game.lines)] for i in range(self.game.columns)]
        for dx in range(len(self.type)):
            for dy in range(len(self.type[dx])):
                if self.type[dx][dy] == 1:
                    if self.x + mx + dx < 0 or self.x + mx + dx >= game.columns or self.y + my + dy < 0 or self.y + my + dy >= game.lines:
                        return False
                    try:
                        board[self.x+dx][self.y+dy] = -1
                    except:
                        return False
        xp = self.x + mx
        yp = self.y + my
        for dx in range(len(self.type)):
            for dy in range(len(self.type[dx])):
                if self.type[dx][dy] == 1:
                    if xp+dx >= self.game.columns or yp+dy >= self.game.lines:
                        return False
                    elif board[xp+dx][yp+dy] != -1:
                        return False
        return True

    def move(self, mx, my):
        for dx in range(len(self.type)):
            for dy in range(len(self.type[dx])):
                if self.type[dx][dy] == 1:
                    self.game.board[self.x+dx][self.y+dy] = -1
        self.x += mx
        self.y += my
        for dx in range(len(self.type)):
            for dy in range(len(self.type[dx])):
                if self.type[dx][dy] == 1:
                    self.game.board[self.x+dx][self.y+dy] = self.color

    def rotate(self):
        pass

    def down(self):
        self.move(0,1) # il tombe

    def update(self):
        if self.testmove(0,1): #gravité
            self.down()
        elif self.isPlaying: #s'il était en jeu, alors on fait apparaître un nouveau tetromino
            self.isPlaying = False
            self.game.spawn()
        self.move(0,0) #ceci va simplement ajouter la pièce telle qu'elle est dans la matrice


class Tetris:
    """
    On définit le Tetris comme une matrice qui se fera actualiser au fil du temps.
    Les cases 0 sont vides.
    Pour n non nul, si self.board[x][y] = n, alors la case est pleine et est de couleur COLOR[n].
    """
    def __init__(self, width, height, level, screen):
        self.lines = height
        self.columns = width
        self.setLevel(level)
        self.board = [[-1]*self.lines for i in range(self.columns)] #matrice de taille C*L qui caractérise le plateau de jeu (colonnes x lignes et pas l'inverse (pour visualiser (O,x,y) en base directe))
        self.playing = None #pièce qu'on joue
        self.score = 0
        self.screen = screen
        self.frameclock = 0
        self.next = self.randomizeNext()
        self.spawn()
        self.ongoing = True
        self.events = []

    def spawn(self):
        if self.playing != None:
            self.playing.update()
        tetroType = self.next.pop()
        if self.next == []:
            self.next =self.randomizeNext()
        nc = len(COLOR)
        col = random.randint(0,nc-1) # on modélise la couleur par un entier qui est son indice dans le tableau COLOR
        tetro = None
        kpossibles = []
        for k in range(self.columns):
            test = True
            for dx in range(len(tetroType)):
                for dy in range(len(tetroType[dx])):
                    if k+dx >= self.columns or self.board[k+dx][dy] != -1:
                        test = False
            if test:
                kpossibles.append(k)
        if kpossibles == []:
            self.ongoing = False
            self.playing = None
        else:
            k = random.choice(kpossibles)
            print(kpossibles)
            tetro = Tetromino(self, tetroType, col, k, 0)
            self.playing = tetro


    def setLevel(self, level):
        self.level = level
        self.T = T(level)

    def incrClock(self):
        self.frameclock += 1
        if self.frameclock == self.T:
            self.frameclock = 0
            self.playing.update()

    def detectInputs(self):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("left")
                    if self.playing.testmove(-1,0):
                        self.playing.move(-1,0)
                if event.key == pygame.K_RIGHT:
                    print("right")
                    if self.playing.testmove(1,0):
                        self.playing.move(1,0)
                if event.key == pygame.K_DOWN:
                    print("down")
                    if self.playing.testmove(0,1):
                        self.playing.move(0,1)
                if event.key == pygame.K_UP:
                    print("rotate")
                    pass #rotations
            if event.type == pygame.KEYUP:
                print("no key is being pressed")


    def randomizeNext(self):
        l = TYPE.copy()
        random.shuffle(l)
        return l

    def update(self):
        drawTextXCentered(self.screen, WIDTH//2, 10, f"Score : {self.score}")
        if self.ongoing:
            self.incrClock()
            self.detectInputs()
            drawText(self.screen, 10, HEIGHT - 40, f"Lv.{self.level}")
            for x in range(self.columns):
                for y in range(self.lines):
                    p = self.board[x][y]
                    if p >= 0:
                        drawSlot(screen, x, y, COLOR[p])
                    else:
                        if (x+y) % 2 == 0:
                            drawSlot(screen, x, y, (88,88,88))
                        else:
                            drawSlot(screen, x, y, (80,80,80))
        else:
            drawTextXCentered(self.screen, WIDTH//2, HEIGHT//2, f"You Lost")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
game = Tetris(C, L, LEVEL, screen)
pygame.display.set_caption("Tetris")

#pygame.mixer.music.load(MUSIC)
#pygame.mixer.music.play(loops=-1)

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
    events = pygame.event.get()
    game.events = events
    for event in events:
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