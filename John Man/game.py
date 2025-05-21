# imports
import pygame
from pygame.locals import *
from board import boards
import math

# create constant variables
TILEWIDTH = 20
TILEHEIGHT = 20
NUMBERROWS = 30
NUMBERCOLS = 33
SCREENWIDTH = TILEWIDTH * NUMBERCOLS
SCREENHEIGHT = TILEHEIGHT * NUMBERROWS
BLACK = (0, 0, 0)

class Object:   # create object class that works as a parent class for all the objects drawn onto the screen at launch
    def __init__(self, surface, row, col, xPos, yPos):  # initialise the object with the stated attributes
        self.__surface = surface
        self.__row = row
        self.__col = col
        self.__xPos = col * TILEWIDTH
        self.__yPos = row * TILEHEIGHT

    def drawSprite(self):   # draws sprite onto the object
        self.__surface.blit(self.__sprite, (self.__xPos, self.__yPos))

class Wall(Object):     # create subclass specifically for walls 
    def __init__(self, surface, row, col, xPos, yPos, wallType):
        super().__init__(surface, row, col, xPos, yPos)
        self.__wallType = wallType  # special variable for the type of wall

# setting up the game including the screen size, clock, surface, and taking the level from the boards file       
pygame.init()
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
timer = pygame.time.Clock()
surface = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
frames = 60
level = boards

# set the title of the window
title = 'John-Man'
pygame.display.set_caption(title) 

objectList = []     # create list to house the objects
def drawGrid():     # create a function to draw all the objects needed on the screen
    for i in range(len(level)):     # loops through the rows in the board file
        for j in range(len(level[i])):  # loops through all the columns for each row 
            return "hi"

running = True  # game loop
while running:
    timer.tick(frames)
    screen.fill(BLACK)

    for event in pygame.event.get():    # check if the game is still running and 
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()
