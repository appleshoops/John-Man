# imports
import pygame
from pygame.locals import *
from board import boards
import math

# create constant variables
TILEWIDTH = 30
TILEHEIGHT = 30
NUMBERROWS = 30
NUMBERCOLS = 32
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

    def drawWall(self, wallType):
        num1 = ((HEIGHT - 50) // 32)
        match wallType:
            case 3:
                pygame.draw.rect(surface, GREEN, )
class Pellet(Object):
    def __init__(self, surface, row, col, xPos, yPos, sprite):
        super().__init__(surface, row, col, xPos, yPos, sprite)

# setting up the game including the screen size, clock, surface, and taking the level from the boards file       
pygame.init()
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
timer = pygame.time.Clock()
surface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
frames = 60
level = boards

# set the title of the window
title = 'John-Man'
pygame.display.set_caption(title) 

sprite_paths = {
    1: "John Man/sprites/grid/1.png"
}
sprites = {key: pygame.image.load(path).convert_alpha() for key, path in sprite_paths.items()}

objectList = []     # create list to house the objects
def drawGrid():     # create a function to draw all the objects needed on the screen
    for i in range(len(level)):     # loops through the rows in the board file
        for j in range(len(level[i])):  # loops through all the columns for each row 
            match level[i][j]:
                case 0:
                    pygame.draw.rect(screen, (0, 0, 0, 0), (j * TILEWIDTH, i * TILEHEIGHT, TILEWIDTH, TILEHEIGHT))
                case 1:
                    sprite = sprites.get(1, sprites[1])  # Ensure sprite for case 1 is loaded
                    wall = Wall(screen, i, j, j * TILEWIDTH, i * TILEHEIGHT, level[i][j], sprite)
                    wall.drawSprite()
                case _:
                    pygame.draw.rect(screen, (0, 0, 0, 0), (j * TILEWIDTH, i * TILEHEIGHT, TILEWIDTH, TILEHEIGHT))
            

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
