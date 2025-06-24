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
    # all the read functions allow the properties of the object to be called
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

    def checkTurns(self):
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
class Pellet(Object): # special class for the pellets that the player collects
    def __init__(self, plane, row, col, x_pos, yPos, sprite):
        super().__init__(plane, row, col, x_pos, yPos, sprite)
class Player(Object): # player is a subclass of object
    def __init__(self, plane, row, col, x_pos, y_pos, direction, direction_command, player_images, points, power, power_counter, player_speed):
        super().__init__(plane, row, col, x_pos, y_pos)
        self.direction = direction
        self.direction_command = direction_command
        self.player_images = player_images
        self.move_counter = 0
        self.points = points
        self.power = power
        self.power_counter = power_counter
        self.eaten_ghosts = [False, False, False, False]
        self.lives = 3
        self.animation_counter = 0
        self.player_speed = player_speed

    @override
    def readPoints(self):
        return self.points
    def drawSprite(self): # draws the player sprite onto the screen
        current_sprite = None
        sprite_index = (self.animation_counter // 3) % len(self.player_images) # cycles through the player animation

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
        
        # Increment the animation counter continuously
        self.animation_counter += 1
    def movePlayer(self):
        for i in range(4):
            if self.direction_command == i and turns_allowed[i]: # check if the player can turn in the direction they want to go
                self.direction = i

        self.move_counter += 1

        if self.move_counter >= self.player_speed: # counter allows me to change speed of the player
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
            level[self.readRow()][self.readCol()] = 0 # remove dot
            self.points += 1 # increase score
            title = f'John Man — Score: {self.points} — Lives: {self.lives} — Speed: {self.player_speed}'
            pygame.display.set_caption(title)
        if current_tile == 2: # Check if the player is on a big dot
            level[self.readRow()][self.readCol()] = 0
            self.points += 10 # big dots get more points
            self.power = True # activate power pellet
            self.power_counter = 0
            title = f'John Man — Score: {self.points} — Lives: {self.lives} — Speed: {self.player_speed}'
            pygame.display.set_caption(title)
        return self.points, self.power, self.power_counter, self.eaten_ghosts
    def powerUp(self): # manages the player's power state
        if self.power and self.power_counter < 600:
            self.power_counter += 1
        elif self.power and self.power_counter >= 600:
            self.power_counter = 0
            self.power = False
            self.eaten_ghosts = [False, False, False, False]
class Ghost(Object): # ghost is a subclass of object
    def __init__(self, plane, row, col, x_pos, y_pos, character, target, box, mortality, ghost_images, direction, speed):
        super().__init__(plane, row, col, x_pos, y_pos)
        self.character = character
        self.target = target
        self.speed = speed  # Speed of the ghost, lower is faster
        self.in_box = box
        self.mortality = mortality  # if the ghost is dead
        self.ghost_images = ghost_images
        self.direction = direction
        self.move_counter = 0
        self.turns_allowed = [False, False, False, False]
        # Remove the drawSprite call from init - this should be called in the game loop
        self.rect = pygame.rect.Rect(0, 0, 36, 36)  # Initialize with default rect

    def moveGhost(self):
        self.turns_allowed = self.checkTurns()
        self.move_counter += 1
        
        # Debug print to see if the function is being called
        # print(f"Ghost {self.character}: move_counter={self.move_counter}, direction={self.direction}, turns_allowed={self.turns_allowed}")
        
        if self.move_counter >= self.speed:
            self.move_counter = 0
            if self.turns_allowed[self.direction]:
                # print(f"Ghost {self.character} moving in direction {self.direction}")
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
                        new_col = NUMBERCOLS - 1
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
            else:
                # If current direction is blocked, find a new valid direction
                print(f"Ghost {self.character} blocked, finding new direction")
                for i in range(4):
                    if self.turns_allowed[i]:
                        self.direction = i
                        print(f"Ghost {self.character} changed direction to {i}")
                        break
    def checkDeadBox(self): # checks if the ghosts are in the dead box
        current_tile = level[self.readRow()][self.readCol()]
        if 13 <= self.readXPos() <= 18 and 14 <= self.readYPos() <= 17: # coordinate range for the dead box
            self.in_box = True
        else:
            self.in_box = False
        return self.in_box
    def findPath(self, player_row, player_col): # finds the shortest path to the player
        #manhattanDistance = ((abs(player_row - self.readRow())) +
        #                     (abs(player_col - self.readCol())))
        available_moves = self.checkTurns()
        short_distance = 9999
        temp_distance = 0
        for i in range(len(available_moves)):
            if available_moves[i]:
                # determines the manhattan distance to the player for each possible direction
                if i == 0:
                    temp_distance = (abs(player_row - self.readRow()) +
                                     abs(player_col - (self.readCol() + 1)))
                if i == 1:
                    temp_distance = (abs(player_row - self.readRow()) +
                                     abs(player_col - (self.readCol() - 1)))
                if i == 2:
                    temp_distance = (abs(player_row - (self.readRow() - 1)) +
                                     abs(player_col - self.readCol()))
                if i == 3:
                    temp_distance = (abs(player_row - (self.readRow() + 1)) +
                                     abs(player_col - self.readCol()))
                # if the distance is shorter than the previous shortest distance, set it as the new shortest distance
                if temp_distance < short_distance:
                    short_distance = temp_distance
                    self.direction = i
                else:
                    pass
        return self.direction


        # use code from player movement

    @override
    def drawSprite(self): # Override the parent method with no additional parameters
        # Get player power and eaten ghosts from the global player object
        player_power = player.power
        eaten_ghosts = player.eaten_ghosts
        
        current_sprite = None

        # Determine which sprite to use
        if self.mortality:  # Ghost is dead (eyes only)
            current_sprite = self.ghost_images[6]
        elif player_power and not eaten_ghosts[self.character]:  # Power pellet active, ghost vulnerable
            current_sprite = self.ghost_images[5]
        elif eaten_ghosts[self.character]:  # Ghost has been eaten but not dead yet
            current_sprite = self.ghost_images[5]
        else:  # Normal ghost state
            current_sprite = self.ghost_images[self.character]

        # Center the sprite in the tile (like the Player class does)
        if current_sprite:
            sprite_width = current_sprite.get_width()
            sprite_height = current_sprite.get_height()
            center_x = self.readXPos() + (TILEWIDTH - sprite_width) // 2
            center_y = self.readYPos() + (TILEHEIGHT - sprite_height) // 2
            self.readSurface().blit(current_sprite, (center_x, center_y))

        # Create collision rect centered on the ghost
        self.rect = pygame.rect.Rect(self.readCentreXPos() - 18, self.readCentreYPos() - 18, 36, 36)
        return self.rect


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
player_speed = 7 # Speed of the player, lower is faster
ghost_speed = 8

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
player = Player(surface, 18, 15, 18 * TILEWIDTH, 15 * TILEHEIGHT, 0, 0, player_sprites, 0, False, 0, player_speed)
def drawPlayer():
    for i in range(1, 4):
        sprite = pygame.image.load(f'sprites/john/{i}.png').convert_alpha()
       #sprite = pygame.transform.scale(sprite, (TILEWIDTH, TILEHEIGHT))  # Scale to tile size (28x28)
        sprite.set_colorkey((255, 255, 255))  # Make white transparent
        player_sprites.append(sprite)
    player.drawSprite()
    player.checkTurns()

ghosts = []
def drawGhosts():
    global ghosts  # Make sure we're using the global ghosts list
    
    # Only create ghosts if the list is empty (first time)
    if not ghosts:
        ghost_sprites = []

        # Load ghost sprites
        for i in range(1, 7):
            sprite = pygame.image.load(f'sprites/ghosts/{i}.png').convert_alpha()
            sprite.set_colorkey((254, 254, 254))
            ghost_sprites.append(sprite)
        
        # Define corner positions for each ghost
        ghost_positions = [
            (2, 2),      # Ghost 0: Top-left corner
            (2, 27),     # Ghost 1: Top-right corner
            (30, 2),     # Ghost 2: Bottom-left corner
            (30, 27)     # Ghost 3: Bottom-right corner
        ]
        
        # Create ghosts at different corner positions
        for i in range(4):
            row, col = ghost_positions[i]
            ghost = Ghost(surface, row, col, col * TILEWIDTH, row * TILEHEIGHT, i, player, False, False, ghost_sprites, 0, ghost_speed)
            ghosts.append(ghost)
    
    # Draw all ghosts
    for ghost in ghosts:
        ghost.drawSprite()  # Call without parameters now

def speedSet():
    score = player.readPoints()
    if player.readPoints() % 282 == 0 and player.readPoints() != 0:
        player.player_speed -= 1
        title = f'John Man — Score: {player.points} — Lives: {player.lives} — Speed: {player.player_speed}'
        pygame.display.set_caption(title)


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
    drawGhosts()
    turns_allowed = player.checkTurns() # Check if the player can turn in each direction
    player.checkCollisions()
    player.powerUp()
    
    # Move all ghosts
    for ghost in ghosts:
        ghost.findPath(player.readRow(), player.readCol())  # Calculate best direction to player
        ghost.moveGhost()  # Move the ghost
    
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