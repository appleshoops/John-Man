# imports
import pygame
from pygame.locals import *
from board import boards
import math

# create constant variables
TILEWIDTH = 16
TILEHEIGHT = 16
NUMBERROWS = 31
NUMBERCOLS = 30
SCREENWIDTH = TILEWIDTH * NUMBERCOLS
SCREENHEIGHT = TILEHEIGHT * NUMBERROWS
BLACK = (0, 0, 0)

class Object():
    def __init__(self, row, col, xPos, yPos):
        self.__row = row
        self.__col = col
        self.__xPos = col * TILEWIDTH
        self.__yPos = row * TILEHEIGHT

pygame.init()
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
timer = pygame.time.Clock()
frames = 60
level = boards

running = True
while running:
    timer.tick(frames)
    screen.fill(BLACK)
    draw_board(boards)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()
