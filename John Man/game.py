# imports
import pygame
from pygame.locals import *
import math

# create constant variables
TILEWIDTH = 16
TILEHEIGHT = 16
NUMBERROWS = 50
NUMBERCOLS = 75
SCREENWIDTH = TILEWIDTH * NUMBERCOLS
SCREENHEIGHT = TILEHEIGHT * NUMBERROWS
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
timer = pygame.time.Clock()
frames = 60

running = True
while running:
    timer.tick(frames)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()
