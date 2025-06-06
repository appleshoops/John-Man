# imports
import pygame

from board import boards
from typing import override


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

class Object:  # create object class that works as a parent class for all the objects drawn onto the screen at launch
    def __init__(self, surface, row, col, xPos, yPos, sprite=None):  # add sprite as an optional parameter
        self.__surface = surface
        self.__row = row
        self.__col = col
        self.__xPos = col * TILEWIDTH
        self.__yPos = row * TILEHEIGHT
        self.__sprite = sprite

    def ReadSurface(self):
        return self.__surface

    def ReadRow(self):
        return self.__row

    def ReadCol(self):
        return self.__col

    def ReadXPos(self):
        return self.__xPos

    def ReadYPos(self):
        return self.__yPos

    def drawSprite(self):  # draws sprite onto the object
        if self.__sprite:
            # Calculate the center position of the tile
            sprite_width = self.__sprite.get_width()
            sprite_height = self.__sprite.get_height()
            center_x = self.__xPos + (TILEWIDTH - sprite_width) // 2
            center_y = self.__yPos + (TILEHEIGHT - sprite_height) // 2
            # Draw the sprite at the center of the tile
            self.__surface.blit(self.__sprite, (center_x, center_y))

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
class Player(Object): # player is a subclass of object from game.py
    def __init__(self, surface, row, col, xPos, yPos, direction, player_images):
        super().__init__(surface, row, col, xPos, yPos)
        self.direction = direction
        self.player_images = player_images

    @override
    def drawSprite(self):
        current_sprite = None
        
        # Get the current sprite based on direction
        if self.direction == 0:  # Right
            current_sprite = self.player_images[counter // 5]
        elif self.direction == 1:  # Left
            current_sprite = pygame.transform.flip(self.player_images[counter // 5], True, False)
        elif self.direction == 2:  # Up
            current_sprite = pygame.transform.rotate(self.player_images[counter // 5], 90)
        elif self.direction == 3:  # Down
            current_sprite = pygame.transform.rotate(self.player_images[counter // 5], 270)
        
        if current_sprite:
            # Center the sprite in the tile
            sprite_width = current_sprite.get_width()
            sprite_height = current_sprite.get_height()
            center_x = self.ReadXPos() + (TILEWIDTH - sprite_width) // 2
            center_y = self.ReadYPos() + (TILEHEIGHT - sprite_height) // 2
            self.ReadSurface().blit(current_sprite, (center_x, center_y))
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
    0: "sprites/grid/0.png",
    1: "sprites/grid/1.png",
    2: "sprites/grid/2.png"
}
sprites = {key: pygame.image.load(path).convert_alpha() for key, path in sprite_paths.items()}

objectList = []     # create list to house the objects
def drawGrid():     # create a function to draw all the objects needed on the screen
    for i in range(len(level)):     # loops through the rows in the board file
        for j in range(len(level[i])):  # loops through all the columns for each row
            x_pos = j * TILEWIDTH
            y_pos = i * TILEHEIGHT

            # pygame.draw.rect(surface, (255, 0, 0), (x_pos, y_pos, TILEWIDTH, TILEHEIGHT), 1)

            match level[i][j]:
                case 0: # blank square
                    pygame.draw.rect(surface, (0, 0, 0, 0), (j * TILEWIDTH, i * TILEHEIGHT, TILEWIDTH, TILEHEIGHT))
                case 1: # little dot
                    sprite = sprites.get(1, sprites[1])
                    pellet = Pellet(surface, i, j, j * TILEWIDTH, i * TILEHEIGHT, sprite)
                    pellet.drawSprite()
                case 2: # lobster (big dot)
                    sprite = sprites.get(2, sprites[2])
                    pellet = Pellet(surface, i, j, j * TILEWIDTH, i * TILEHEIGHT, sprite)
                    pellet.drawSprite()
                case 3:
                    wall = Wall(surface, i, j, x_pos, y_pos, 3)
                    wall.drawWall()
                case 4:
                    wall = Wall(surface, i, j, x_pos, y_pos, 4)
                    wall.drawWall()
                case 5:  # Top right corner
                    wall = Wall(surface, i, j, x_pos, y_pos, 5)
                    wall.drawWall()
                case 6:  # Top left corner
                    wall = Wall(surface, i, j, x_pos, y_pos, 6)
                    wall.drawWall()
                case 7:  # Bottom left corner
                    wall = Wall(surface, i, j, x_pos, y_pos, 7)
                    wall.drawWall()
                case 8:  # Bottom right corner
                    wall = Wall(surface, i, j, x_pos, y_pos, 8)
                    wall.drawWall()
                case _:
                    pygame.draw.rect(screen, (0, 0, 0, 0), (j * TILEWIDTH, i * TILEHEIGHT, TILEWIDTH, TILEHEIGHT))

def drawPlayer():
    player_images = []
    for i in range(1, 4):
        sprite = pygame.image.load(f'sprites/john/{i}.png').convert_alpha()
        sprite = pygame.transform.scale(sprite, (TILEWIDTH, TILEHEIGHT))  # Scale to tile size (28x28)
        sprite.set_colorkey((255, 255, 255))  # Make white transparent
        player_images.append(sprite)

    player = Player(surface, 18, 15, 18 * TILEWIDTH, 15 * TILEHEIGHT, 0, player_images)
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