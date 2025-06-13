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

# set the title of the window
title = 'John-Man'
pygame.display.set_caption(title)

class Object:  # create object class that works as a parent class for all the objects drawn onto the screen at launch
    def __init__(self, plane, row, col, xPos, yPos, sprite=None):  # add sprite as an optional parameter
        self.__surface = plane
        self.__row = row
        self.__col = col
        self.__xPos = col * TILEWIDTH
        self.__yPos = row * TILEHEIGHT
        self.__sprite = sprite

    def readSurface(self):
        return self.__surface

    def readRow(self):
        return self.__row

    def readCol(self):
        return self.__col

    def readXPos(self):
        return self.__xPos

    def readYPos(self):
        return self.__yPos

    def readCentrePos(self):
        center_x = self.__xPos + TILEWIDTH // 2
        center_y = self.__yPos + TILEHEIGHT // 2
        return center_x, center_y

    def readCentreXPos(self):
        center_x = self.__xPos + TILEWIDTH // 2
        return center_x

    def readCentreYPos(self):
        center_y = self.__yPos + TILEHEIGHT // 2
        return center_y

    def drawSprite(self):  # draws sprite onto the object
        if self.__sprite:
            pygame.draw.circle(self.__surface, GREEN, self.readCentrePos(), 2)
            # Calculate the center position of the tile
            sprite_width = self.__sprite.get_width()
            sprite_height = self.__sprite.get_height()
            center_x = self.__xPos + (TILEWIDTH - sprite_width) // 2
            center_y = self.__yPos + (TILEHEIGHT - sprite_height) // 2
            # Draw the sprite at the center of the tile
            self.__surface.blit(self.__sprite, (center_x, center_y))
class Wall(Object):     # create subclass specifically for walls 
    def __init__(self, plane, row, col, x_pos, yPos, wallType):
        super().__init__(plane, row, col, x_pos, yPos)
        self.__wallType = wallType  # special variable for the type of wall

    def drawWall(self):
        tileWidth = TILEWIDTH
        tileHeight = TILEHEIGHT
        centerX = self.readXPos() + tileWidth // 2
        centerY = self.readYPos() + tileHeight // 2
        match self.__wallType:
            case 3:  # Vertical line
                pygame.draw.line(
                    self.readSurface(),
                    GREEN,
                    (centerX, self.readYPos() + WALL_OFFSET),
                    (centerX, self.readYPos() + tileHeight - WALL_OFFSET),
                    WALL_THICKNESS
                )
            case 4:  # Horizontal line
                pygame.draw.line(
                    self.readSurface(),
                    GREEN,
                    (self.readXPos() + WALL_OFFSET, centerY),
                    (self.readXPos() + tileWidth - WALL_OFFSET, centerY),
                    WALL_THICKNESS
                )
            case 5:  # Top right corner
                pygame.draw.line(
                    self.readSurface(),
                    GREEN,
                    (self.readXPos() + WALL_OFFSET, centerY),
                    (centerX, centerY),
                    WALL_THICKNESS
                )
                pygame.draw.line(
                    self.readSurface(),
                    GREEN,
                    (centerX, centerY),
                    (centerX, self.readYPos() + tileHeight - WALL_OFFSET),
                    WALL_THICKNESS
                )
            case 6:  # Top left corner
                pygame.draw.line(
                    self.readSurface(),
                    GREEN,
                    (centerX, self.readYPos() + tileHeight - WALL_OFFSET),
                    (centerX, centerY),
                    WALL_THICKNESS
                )
                pygame.draw.line(
                    self.readSurface(),
                    GREEN,
                    (centerX, centerY),
                    (self.readXPos() + tileWidth - WALL_OFFSET, centerY),
                    WALL_THICKNESS
                )
            case 7:  # Bottom left corner
                pygame.draw.line(
                    self.readSurface(),
                    GREEN,
                    (centerX, self.readYPos() + WALL_OFFSET),
                    (centerX, centerY),
                    WALL_THICKNESS
                )
                pygame.draw.line(
                    self.readSurface(),
                    GREEN,
                    (centerX, centerY),
                    (self.readXPos() + tileWidth - WALL_OFFSET, centerY),
                    WALL_THICKNESS
                )
            case 8:  # Bottom right corner
                pygame.draw.line(
                    self.readSurface(),
                    GREEN,
                    (centerX, self.readYPos() + WALL_OFFSET),
                    (centerX, centerY),
                    WALL_THICKNESS
                )
                pygame.draw.line(
                    self.readSurface(),
                    GREEN,
                    (centerX, centerY),
                    (self.readXPos() + WALL_OFFSET, centerY),
                    WALL_THICKNESS
                )
class Pellet(Object):
    def __init__(self, plane, row, col, x_pos, yPos, sprite):
        super().__init__(plane, row, col, x_pos, yPos, sprite)
class Player(Object): # player is a subclass of object from game.py
    def __init__(self, plane, row, col, x_pos, y_pos, direction, direction_command, player_images, points, power, power_counter):
        super().__init__(plane, row, col, x_pos, y_pos)
        self.direction = direction
        self.direction_command = direction_command
        self.player_images = player_images
        self.player_speed = 7 # Speed of the player, lower is faster
        self.move_counter = 0
        self.points = points
        self.power = power
        self.power_counter = power_counter
        self.eaten_ghosts = [False, False, False, False]
        self.lives = 3

    @override
    def drawSprite(self):
        current_sprite = None
        # Get the current sprite based on direction
        # Use a smaller divisor for smoother animation (was 4, now 2)
        sprite_index = (counter // 3) % len(self.player_images)
        
        if self.direction == 0:  # Right
            current_sprite = self.player_images[sprite_index]
        elif self.direction == 1:  # Left
            current_sprite = pygame.transform.flip(self.player_images[sprite_index], True, False)
        elif self.direction == 2:  # Up
            current_sprite = pygame.transform.rotate(self.player_images[sprite_index], 90)
        elif self.direction == 3:  # Down
            current_sprite = pygame.transform.rotate(self.player_images[sprite_index], 270)
        
        if current_sprite:
            # Center the sprite in the tile
            sprite_width = current_sprite.get_width()
            sprite_height = current_sprite.get_height()
            center_x = self.readXPos() + (TILEWIDTH - sprite_width) // 2
            center_y = self.readYPos() + (TILEHEIGHT - sprite_height) // 2
            self.readSurface().blit(current_sprite, (center_x, center_y))
    def checkPosition(self):
        turns = [False, False, False, False]  # [right, left, up, down]
        
        # Get current row and column positions
        current_row = self.readRow()
        current_col = self.readCol()

        next_col = current_col + 1
        if next_col < NUMBERCOLS and level[current_row][next_col] < 3:
            turns[0] = True
        
        # Check left movement  
        next_col = current_col - 1
        if next_col >= 0 and level[current_row][next_col] < 3:
            turns[1] = True
        
        # Check up movement
        next_row = current_row - 1
        if next_row >= 0 and level[next_row][current_col] < 3:
            turns[2] = True
        
        # Check down movement
        next_row = current_row + 1
        if next_row < NUMBERROWS and level[next_row][current_col] < 3:
            turns[3] = True
        
        return turns
    def movePlayer(self):
        for i in range(4):
            if self.direction_command == i and turns_allowed[i]: # check if the player can turn in the direction they want to go
                self.direction = i

        self.move_counter += 1

        if self.move_counter >= self.player_speed:
            self.move_counter = 0

            if turns_allowed[self.direction]:
                if self.direction == 0:  # Moving right
                    current_col = self.readCol()
                    new_col = current_col + 1
                    if new_col >= NUMBERCOLS:
                        new_col = 0
                    self._Object__col = new_col
                    self._Object__xPos = new_col * TILEWIDTH

                elif self.direction == 1:  # Moving left
                    current_col = self.readCol()
                    new_col = current_col - 1
                    if new_col < 0:
                        new_col = NUMBERCOLS - 1  # Teleport to right side
                    self._Object__col = new_col
                    self._Object__xPos = new_col * TILEWIDTH

                elif self.direction == 2:  # Moving up
                    current_row = self.readRow()
                    new_row = current_row - 1
                    if new_row >= 0:
                        self._Object__row = new_row
                        self._Object__yPos = new_row * TILEHEIGHT

                elif self.direction == 3:  # Moving down
                    current_row = self.readRow()
                    new_row = current_row + 1
                    if new_row < NUMBERROWS:
                        self._Object__row = new_row
                        self._Object__yPos = new_row * TILEHEIGHT
    def checkCollisions(self):
        current_tile = level[self.readRow()][self.readCol()]
        if current_tile == 1: # Check if the player is on a dot
            level[self.readRow()][self.readCol()] = 0
            self.points += 1
            title = f'John Man — Score: {self.points} — Lives: {self.lives}'
            pygame.display.set_caption(title)
        if current_tile == 2: # Check if the player is on a dot
            level[self.readRow()][self.readCol()] = 0
            self.points += 10
            self.power = True
            self.power_counter = 0
            title = f'John Man — Score: {self.points} — Lives: {self.lives}'
            pygame.display.set_caption(title)
        return self.points, self.power, self.power_counter, self.eaten_ghosts
    def powerUp(self):
        if self.power and self.power_counter < 600:
            self.power_counter += 1
        elif self.power and self.power_counter >= 600:
            self.power_counter = 0
            self.power = False
            self.eaten_ghosts = [False, False, False, False]
class Ghost(Object):
    def __init__(self, plane, row, col, x_pos, y_pos, character, target, box, mortality):
        super().__init__(plane, row, col, x_pos, y_pos)
        self.character = character
        self.target = target
        self.speed = 7  # Speed of the ghost, lower is faster
        self.in_box = box
        self.mortality = mortality  # if the ghost is dead



# setting up the game including the screen size, clock, surface, and taking the level from the boards file
pygame.init()
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
timer = pygame.time.Clock()
surface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
frames = 60
level = boards
counter = 0
turns_allowed = [False, False, False, False]  # [right, left, up, down]
startup_counter = 0

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

            #pygame.draw.rect(surface, (255, 0, 0), (x_pos, y_pos, TILEWIDTH, TILEHEIGHT), 1)
            #dots_remaining =
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

player_sprites = []
player = Player(surface, 18, 15, 18 * TILEWIDTH, 15 * TILEHEIGHT, 0, 0, player_sprites, 0, False, 0)
def drawPlayer():
    for i in range(1, 4):
        sprite = pygame.image.load(f'sprites/john/{i}.png').convert_alpha()
       #sprite = pygame.transform.scale(sprite, (TILEWIDTH, TILEHEIGHT))  # Scale to tile size (28x28)
        sprite.set_colorkey((255, 255, 255))  # Make white transparent
        player_sprites.append(sprite)
    player.drawSprite()
    player.checkPosition()

running = True  # game loop
while running:
    timer.tick(frames)

    if counter < 15:
        counter += 1
    else:
        counter = 0

    screen.fill(BLACK)
    drawGrid()
    drawPlayer()
    turns_allowed = player.checkPosition() # Check if the player can turn in each direction
    player.checkCollisions()
    player.powerUp()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.direction_command = 0
            if event.key == pygame.K_LEFT:
                player.direction_command = 1
            if event.key == pygame.K_UP:
                player.direction_command = 2
            if event.key == pygame.K_DOWN:
                player.direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and player.direction_command == 0:
                player.direction_command = 0
            if event.key == pygame.K_LEFT and player.direction_command == 1:
                player.direction_command = 1
            if event.key == pygame.K_UP and player.direction_command == 2:
                player.direction_command = 2
            if event.key == pygame.K_DOWN and player.direction_command == 3:
                player.direction_command = 3
    player.movePlayer()
    pygame.display.flip()
pygame.quit()