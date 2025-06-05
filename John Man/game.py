# imports
import pygame
from pygame.locals import *
from board import boards
from john import Player
from object import Object
import math


# create constant variables
TILEWIDTH = 28
TILEHEIGHT = 28
NUMBERROWS = 32
NUMBERCOLS = 30
SCREENWIDTH = TILEWIDTH * NUMBERCOLS
SCREENHEIGHT = TILEHEIGHT * NUMBERROWS
BLACK = (0, 0, 0)
GREEN = (150, 255, 197)
WALL_THICKNESS = 3
WALL_OFFSET = 0  # Removed offset to make walls connect properly

class Wall(Object):     # create subclass specifically for walls 
    def __init__(self, surface, row, col, xPos, yPos, wallType):
        super().__init__(surface, row, col, xPos, yPos)
        self.__wallType = wallType  # special variable for the type of wall

    def drawWall(self):
        tileWidth = TILEWIDTH
        tileHeight = TILEHEIGHT
        centerX = self.ReadXPos() + tileWidth // 2
        centerY = self.ReadYPos() + tileHeight // 2
        match self.__wallType:
            case 3:  # Vertical line
                pygame.draw.line(
                    self.ReadSurface(),
                    GREEN,
                    (centerX, self.ReadYPos() + WALL_OFFSET),
                    (centerX, self.ReadYPos() + tileHeight - WALL_OFFSET),
                    WALL_THICKNESS
                )
            case 4:  # Horizontal line
                pygame.draw.line(
                    self.ReadSurface(),
                    GREEN,
                    (self.ReadXPos() + WALL_OFFSET, centerY),
                    (self.ReadXPos() + tileWidth - WALL_OFFSET, centerY),
                    WALL_THICKNESS
                )
            case 5:  # Top right corner
                pygame.draw.line(
                    self.ReadSurface(),
                    GREEN,
                    (self.ReadXPos() + WALL_OFFSET, centerY),
                    (centerX, centerY),
                    WALL_THICKNESS
                )
                pygame.draw.line(
                    self.ReadSurface(),
                    GREEN,
                    (centerX, centerY),
                    (centerX, self.ReadYPos() + tileHeight - WALL_OFFSET),
                    WALL_THICKNESS
                )
            case 6:  # Top left corner
                pygame.draw.line(
                    self.ReadSurface(),
                    GREEN,
                    (centerX, self.ReadYPos() + tileHeight - WALL_OFFSET),
                    (centerX, centerY),
                    WALL_THICKNESS
                )
                pygame.draw.line(
                    self.ReadSurface(),
                    GREEN,
                    (centerX, centerY),
                    (self.ReadXPos() + tileWidth - WALL_OFFSET, centerY),
                    WALL_THICKNESS
                )
            case 7:  # Bottom left corner
                pygame.draw.line(
                    self.ReadSurface(),
                    GREEN,
                    (centerX, self.ReadYPos() + WALL_OFFSET),
                    (centerX, centerY),
                    WALL_THICKNESS
                )
                pygame.draw.line(
                    self.ReadSurface(),
                    GREEN,
                    (centerX, centerY),
                    (self.ReadXPos() + tileWidth - WALL_OFFSET, centerY),
                    WALL_THICKNESS
                )
            case 8:  # Bottom right corner
                pygame.draw.line(
                    self.ReadSurface(),
                    GREEN,
                    (centerX, self.ReadYPos() + WALL_OFFSET),
                    (centerX, centerY),
                    WALL_THICKNESS
                )
                pygame.draw.line(
                    self.ReadSurface(),
                    GREEN,
                    (centerX, centerY),
                    (self.ReadXPos() + WALL_OFFSET, centerY),
                    WALL_THICKNESS
                )
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
counter = 0

# set the title of the window
title = 'John-Man'
pygame.display.set_caption(title) 

sprite_paths = {
    1: "John Man/sprites/grid/1.png",
    2: "John Man/sprites/grid/2.png",
    3: "John Man/sprites/john/3.png"
}
sprites = {key: pygame.image.load(path).convert_alpha() for key, path in sprite_paths.items()}


objectList = []     # create list to house the objects
def drawGrid():     # create a function to draw all the objects needed on the screen
    for i in range(len(level)):     # loops through the rows in the board file
        for j in range(len(level[i])):  # loops through all the columns for each row 
            xPos = j * TILEWIDTH
            yPos = i * TILEHEIGHT
            
            pygame.draw.rect(surface, (255, 0, 0), (xPos, yPos, TILEWIDTH, TILEHEIGHT), 1)

            match level[i][j]:
                case 0:
                    pygame.draw.rect(surface, (0, 0, 0, 0), (j * TILEWIDTH, i * TILEHEIGHT, TILEWIDTH, TILEHEIGHT))
                case 1:
                    sprite = sprites.get(1, sprites[1])
                    pellet = Pellet(surface, i, j, j * TILEWIDTH, i * TILEHEIGHT, sprite)
                    pellet.drawSprite()
                case 2:
                    sprite = sprites.get(2, sprites[2])
                    pellet = Pellet(surface, i, j, j * TILEWIDTH, i * TILEHEIGHT, sprite)
                    pellet.drawSprite()
                case 3:
                    wall = Wall(surface, i, j, xPos, yPos, 3)
                    wall.drawWall()
                case 4:
                    wall = Wall(surface, i, j, xPos, yPos, 4)
                    wall.drawWall()
                case 5:  # Top right corner
                    wall = Wall(surface, i, j, xPos, yPos, 5)
                    wall.drawWall()
                case 6:  # Top left corner
                    wall = Wall(surface, i, j, xPos, yPos, 6)
                    wall.drawWall()
                case 7:  # Bottom left corner
                    wall = Wall(surface, i, j, xPos, yPos, 7)
                    wall.drawWall()
                case 8:  # Bottom right corner
                    wall = Wall(surface, i, j, xPos, yPos, 8)
                    wall.drawWall()
                case _:
                    pygame.draw.rect(screen, (0, 0, 0, 0), (j * TILEWIDTH, i * TILEHEIGHT, TILEWIDTH, TILEHEIGHT))

def drawPlayer():
    player_images = []
    for i in range(1, 4):
        self.player_images.append(pygame.transform.scale(pygame.image.load(f'John Man/sprites/john/{i}.png'), (45, 45))) # load the player sprites into a list

    player = Player(surface, 19, 15, 19 * TILEWIDTH, 15 * TILEHEIGHT, 0, player_images)
    player.drawSprite()

running = True  # game loop
while running: 
    timer.tick(frames)
    screen.fill(BLACK)
    drawGrid()
    drawPlayer()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()
