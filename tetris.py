import pygame
import os
import sys



WIDTH = 500
LENGTH = 500
MUSIC = "music.mp3"

class Tetris:
    def __init__(self):
        pass

pygame.init()
screen = pygame.display.set_mode((WIDTH, LENGTH))
pygame.display.set_caption("Tetris")

pygame.mixer.music.load(MUSIC)
pygame.mixer.music.play(loops=-1)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((20, 20, 20))
    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()
sys.exit()