# imports
import pygame
from pygame.locals import *
from board import boards
import math

# create constant variables
TILEWIDTH = 30
TILEHEIGHT = 30
NUMBERROWS = 30
NUMBERCOLS = 30
SCREENWIDTH = TILEWIDTH * NUMBERCOLS
SCREENHEIGHT = TILEHEIGHT * NUMBERROWS
BLACK = (0, 0, 0)

class Object:   # create object class that works as a parent class for all the objects drawn onto the screen at launch
    def __init__(self, surface, row, col, xPos, yPos, sprite=None):  # add sprite as an optional parameter
        self.__surface = surface
        self.__row = row
        self.__col = col
        self.__xPos = col * TILEWIDTH
        self.__yPos = row * TILEHEIGHT
        self.__sprite = sprite

    def drawSprite(self):   # draws sprite onto the object
        if self.__sprite:
            self.__surface.blit(self.__sprite, (self.__xPos, self.__yPos))

class Wall(Object):     # create subclass specifically for walls 
    def __init__(self, surface, row, col, xPos, yPos, wallType, sprite):
        super().__init__(surface, row, col, xPos, yPos, sprite)
        self.__wallType = wallType  # special variable for the type of wall

# setting up the game including the screen size, clock, surface, and taking the level from the boards file       
pygame.init()
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
timer = pygame.time.Clock()
surface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE)
frames = 60
level = boards

emptySprite = pygame.image.load("John Man/sprites/grid/0.png").convert_alpha()
vertLeftSprite = pygame.image.load("John Man/sprites/grid/3.png").convert_alpha()
horizontalTopSprite = pygame.image.load("John Man/sprites/grid/4.png").convert_alpha()
topRightSprite = pygame.image.load("John Man/sprites/grid/5.png").convert_alpha()
topLeftSprite = pygame.image.load("John Man/sprites/grid/6.png").convert_alpha()
bottomLeftSprite = pygame.image.load("John Man/sprites/grid/7.png").convert_alpha()
bottomRightSprite = pygame.image.load("John Man/sprites/grid/8.png").convert_alpha()
vertRightSprite = pygame.image.load("John Man/sprites/grid/10.png").convert_alpha()
horizontalBottomSprite = pygame.image.load("John Man/sprites/grid/11.png").convert_alpha()
bottomLeftSmallSprite = pygame.image.load("John Man/sprites/grid/12.png").convert_alpha()
bottomRightSmallSprite = pygame.image.load("John Man/sprites/grid/13.png").convert_alpha()

# set the title of the window
title = 'John-Man'
pygame.display.set_caption(title) 

objectList = []     # create list to house the objects
def drawGrid():     # create a function to draw all the objects needed on the screen
    for i in range(len(level)):     # loops through the rows in the board file
        for j in range(len(level[i])):  # loops through all the columns for each row 
            match level[i][j]:
                case 1:
                    sprite = emptySprite
                case 3:
                    sprite = vertLeftSprite
                case 4:
                    sprite = horizontalTopSprite
                case 5:
                    sprite = topRightSprite
                case 6:
                    sprite = topLeftSprite
                case 7:
                    sprite = bottomLeftSprite
                case 8:
                    sprite = bottomRightSprite
                case 10:
                    sprite = vertRightSprite
                case 11:
                    sprite = horizontalBottomSprite
                case 12:
                    sprite = bottomLeftSmallSprite
                case 13:
                    sprite = bottomRightSmallSprite
                case _:
                    sprite = emptySprite
            wall = Wall(screen, i, j, j * TILEWIDTH, i * TILEHEIGHT, level[i][j], sprite)
            wall.drawSprite()

running = True  # game loop
while running: 
    timer.tick(frames)
    screen.fill(BLACK)
    drawGrid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()
