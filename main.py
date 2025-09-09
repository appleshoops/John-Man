# imports
import pygame
import random
import asyncio
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

# setting up the game including the screen size, clock, surface, and taking the level from the boards file
pygame.init()
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])
timer = pygame.time.Clock()
surface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
frames = 60
level = []
for row in boards:
    level.append(row.copy())  # Create a copy of each row to avoid modifying the original board
counter = 0
turns_allowed = [False, False, False, False]  # [right, left, up, down]
startup_counter = 0
player_speed = 7 # Speed of the player, lower is faster
ghost_speed = 8

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
    def checkGhostCollisions(self):
        for ghost in ghosts:
            # Check if player and ghost positions overlap
            player_rect = pygame.rect.Rect(self.readCentreXPos() - 18, self.readCentreYPos() - 18, 36, 36)

            if player_rect.colliderect(ghost.rect):
                if self.power and not self.eaten_ghosts[ghost.character]:
                    # Player eats ghost
                    self.eaten_ghosts[ghost.character] = True
                    self.points += 100  # Points for eating a ghost

                    # Make ghost return to box
                    ghost.mortality = True

                    # Reset ghost position to their corners
                    if ghost.character == 0:
                        ghost._Object__row = 2
                        ghost._Object__col = 2
                    elif ghost.character == 1:
                        ghost._Object__row = 2
                        ghost._Object__col = 27
                    elif ghost.character == 2:
                        ghost._Object__row = 30
                        ghost._Object__col = 2
                    else:
                        ghost._Object__row = 30
                        ghost._Object__col = 27

                    # Update pixel positions
                    ghost._Object__xPos = ghost._Object__col * TILEWIDTH
                    ghost._Object__yPos = ghost._Object__row * TILEHEIGHT

                elif not self.power and not ghost.mortality:
                    # Ghost eats player
                    self.lives -= 1
                    title = f'John Man — Score: {player.points} — Lives: {player.lives} — Speed: {player.player_speed}'
                    pygame.display.set_caption(title)
                    if self.lives > 0:
                        # Reset player position
                        self._Object__row = 18
                        self._Object__col = 15
                        self._Object__xPos = 15 * TILEWIDTH
                        self._Object__yPos = 18 * TILEHEIGHT
                        self.direction = 0
                        self.direction_command = 0
                    else:
                        # Game over
                        global running
                        running = False
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

            for i, eaten in enumerate(self.eaten_ghosts): # reset eaten ghosts when power up ends
                if eaten:
                    for ghost in ghosts:
                        if ghost.character == i:
                            ghost.mortality = False

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
                self.findRandomDirection() # if the ghost can't turn in the direction it wants to go, find a random direction
    def checkDeadBox(self): # checks if the ghosts are in the dead box
        current_tile = level[self.readRow()][self.readCol()]
        if 13 <= self.readXPos() <= 18 and 14 <= self.readYPos() <= 17: # coordinate range for the dead box
            self.in_box = True
        else:
            self.in_box = False
        return self.in_box
    def findPath(self, player_row, player_col):
        self.turns_allowed = self.checkTurns()

        # Give each ghost a distinct personality
        if self.character == 0:  # Red ghost (Blinky) - Direct chaser
            # Almost always pursues player directly
            randomness_factor = 0.05
            target_row = player_row
            target_col = player_col
        elif self.character == 1:  # Pink ghost (Pinky) - Ambusher
            # Tries to get ahead of the player
            randomness_factor = 0.15
            # Target 4 tiles ahead of player based on player's direction
            if player.direction == 0:  # Right
                target_row = player_row
                target_col = (player_col + 4) % NUMBERCOLS
            elif player.direction == 1:  # Left
                target_row = player_row
                target_col = (player_col - 4) % NUMBERCOLS
            elif player.direction == 2:  # Up
                target_row = max(0, player_row - 4)
                target_col = player_col
            elif player.direction == 3:  # Down
                target_row = min(NUMBERROWS - 1, player_row + 4)
                target_col = player_col
        elif self.character == 2:  # Blue ghost (Inky) - Complex targeting
            # Targets position based on both player and red ghost
            randomness_factor = 0.25
            if len(ghosts) > 0 and self.character != 0:  # Ensure red ghost exists and this isn't the red ghost
                red_ghost = None
                for ghost in ghosts:
                    if ghost.character == 0:
                        red_ghost = ghost
                        break

                if red_ghost:
                    # Target is vector from red ghost to player, doubled
                    target_row = player_row + (player_row - red_ghost.readRow())
                    target_row = max(0, min(target_row, NUMBERROWS - 1))
                    target_col = player_col + (player_col - red_ghost.readCol())
                    target_col = max(0, min(target_col, NUMBERCOLS - 1))
                else:
                    # Fallback if red ghost not found
                    target_row = player_row
                    target_col = player_col
            else:
                target_row = player_row
                target_col = player_col
        else:  # Orange ghost (Clyde) - Shy
            # Pursues player directly when far, but wanders when close
            randomness_factor = 0.35
            distance_to_player = abs(player_row - self.readRow()) + abs(player_col - self.readCol())
            if distance_to_player < 8:  # When close to player, retreat to corner
                target_row = 30
                target_col = 2
            else:  # When far, chase directly
                target_row = player_row
                target_col = player_col

        # When player has power, all ghosts run away (but with different patterns)
        if player.power and not player.eaten_ghosts[self.character]:
            # Different ghosts have different "scatter" corners when fleeing
            if self.character == 0:
                target_row, target_col = 2, 2  # Top-left
            elif self.character == 1:
                target_row, target_col = 2, 27  # Top-right
            elif self.character == 2:
                target_row, target_col = 30, 2  # Bottom-left
            else:
                target_row, target_col = 30, 27  # Bottom-right

            # Increase randomness when fleeing to make movement less predictable
            randomness_factor += 0.2

        # Random movement chance
        if random.random() < randomness_factor:
            self.findRandomDirection()
            return self.direction

        # Find best direction towards target
        best_direction = -1

        if player.power and not player.eaten_ghosts[self.character]:
            # Run away - maximize distance to target
            max_distance = -float('inf')

            for i in range(4):
                if self.turns_allowed[i]:
                    if i == 0:  # Right
                        temp_row = self.readRow()
                        temp_col = (self.readCol() + 1) % NUMBERCOLS
                    elif i == 1:  # Left
                        temp_row = self.readRow()
                        temp_col = (self.readCol() - 1) % NUMBERCOLS
                    elif i == 2:  # Up
                        temp_row = max(0, self.readRow() - 1)
                        temp_col = self.readCol()
                    elif i == 3:  # Down
                        temp_row = min(NUMBERROWS - 1, self.readRow() + 1)
                        temp_col = self.readCol()

                    # Calculate Manhattan distance to the target
                    temp_distance = abs(target_row - temp_row) + abs(target_col - temp_col)

                    # Choose direction that maximizes distance
                    if temp_distance > max_distance:
                        max_distance = temp_distance
                        best_direction = i
        else:
            # Chase - minimize distance to target
            short_distance = float('inf')

            for i in range(4):
                if self.turns_allowed[i]:
                    if i == 0:  # Right
                        temp_row = self.readRow()
                        temp_col = (self.readCol() + 1) % NUMBERCOLS
                    elif i == 1:  # Left
                        temp_row = self.readRow()
                        temp_col = (self.readCol() - 1) % NUMBERCOLS
                    elif i == 2:  # Up
                        temp_row = max(0, self.readRow() - 1)
                        temp_col = self.readCol()
                    elif i == 3:  # Down
                        temp_row = min(NUMBERROWS - 1, self.readRow() + 1)
                        temp_col = self.readCol()

                    # Calculate Manhattan distance to target
                    temp_distance = abs(target_row - temp_row) + abs(target_col - temp_col)

                    # Choose direction that minimizes distance
                    if temp_distance < short_distance:
                        short_distance = temp_distance
                        best_direction = i

        # Update direction if a valid one was found
        if best_direction != -1:
            self.direction = best_direction
        else:
            self.findRandomDirection()

        return self.direction
        # use code from player movement
    def findRandomDirection(self):
        self.turns_allowed = self.checkTurns()

        # Get all valid directions
        valid_dirs = [i for i, valid in enumerate(self.turns_allowed) if valid]

        if not valid_dirs:
            # Ghost is stuck (shouldn't happen)
            # Try to reset position to a known safe location
            if self.character == 0:
                self._Object__row = 2
                self._Object__col = 2
                self._Object__xPos = 2 * TILEWIDTH
                self._Object__yPos = 2 * TILEHEIGHT
            elif self.character == 1:
                self._Object__row = 2
                self._Object__col = 27
                self._Object__xPos = 27 * TILEWIDTH
                self._Object__yPos = 2 * TILEHEIGHT
            elif self.character == 2:
                self._Object__row = 30
                self._Object__col = 2
                self._Object__xPos = 2 * TILEWIDTH
                self._Object__yPos = 30 * TILEHEIGHT
            elif self.character == 3:
                self._Object__row = 30
                self._Object__col = 27
                self._Object__xPos = 27 * TILEWIDTH
                self._Object__yPos = 30 * TILEHEIGHT
            return

        # Different ghosts have different movement patterns
        # Character 0: Prefers continuing straight
        # Character 1: Slightly prefers continuing straight
        # Character 2: Completely random
        # Character 3: Prefers turning
        continue_straight_chance = 0.7 - (self.character * 0.2)

        if self.direction in valid_dirs and random.random() < continue_straight_chance:
            # Continue in same direction
            return

        # Otherwise choose a random valid direction
        self.direction = random.choice(valid_dirs)
    @override
    def drawSprite(self): # Override the parent method with no additional parameters
        # Get player power and eaten ghosts from the global player object
        player_power = player.power
        eaten_ghosts = player.eaten_ghosts
        
        current_sprite = None

        # Determine which sprite to use
        if self.mortality:  # Ghost is dead (eyes only)
            current_sprite = self.ghost_images[5]
        elif player_power and not eaten_ghosts[self.character]:
            current_sprite = self.ghost_images[4]  # Scared ghost sprite
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


def check_level_complete():
    dots_remaining = False

    # Check if any dots remain in the level
    for row in level:
        if 1 in row or 2 in row:
            dots_remaining = True
            break

    if not dots_remaining:
        # Level complete - reset the board and increase speed
        player.lives += 1  # Give player an extra life if they complete the level
        reset_level()
        increase_speed()
        return True
    return False


def reset_level():
    global level, boards

    # Instead of trying to copy boards, just reload the level from the board.py file
    from board import boards as original_boards

    # Reset the level with fresh data from import
    level = []
    for row in original_boards:
        level.append(row.copy())

    # Reset ghost positions
    for i, ghost in enumerate(ghosts):
        # Reset ghosts to their starting positions
        if i == 0:  # Ghost 0: Top-left
            ghost._Object__row = 2
            ghost._Object__col = 2
        elif i == 1:  # Ghost 1: Top-right
            ghost._Object__row = 2
            ghost._Object__col = 27
        elif i == 2:  # Ghost 2: Bottom-left
            ghost._Object__row = 30
            ghost._Object__col = 2
        elif i == 3:  # Ghost 3: Bottom-right
            ghost._Object__row = 30
            ghost._Object__col = 27

        # Update pixel positions
        ghost._Object__xPos = ghost._Object__col * TILEWIDTH
        ghost._Object__yPos = ghost._Object__row * TILEHEIGHT
        ghost.mortality = False  # Reset mortality

    # Reset player position
    player._Object__row = 18
    player._Object__col = 15
    player._Object__xPos = 15 * TILEWIDTH
    player._Object__yPos = 18 * TILEHEIGHT
    player.direction = 0
    player.direction_command = 0
    player.power = False
    player.power_counter = 0
    player.eaten_ghosts = [False, False, False, False]


def increase_speed():
    global player_speed, ghost_speed

    # Decrease speed by 1 but keep minimum of 3 to prevent issues
    player_speed = max(3, player_speed - 1)
    player.player_speed = player_speed  # Ensure player instance gets updated speed

    # Make ghosts faster but not too fast
    ghost_speed = max(3, ghost_speed - 1)

    # Update each ghost's speed attribute
    for ghost in ghosts:
        ghost.speed = ghost_speed

    # Update title with new speed level
    title = f'John Man — Score: {player.points} — Lives: {player.lives} — Speed: {player_speed}'
    pygame.display.set_caption(title)


async def main():
    waiting_for_start = True

    # Show start screen
    while waiting_for_start:
        screen.fill(BLACK)

        # Draw start message
        font = pygame.font.Font(None, 36)
        text = font.render("Click to Start John-Man!", True, GREEN)
        text_rect = text.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2))
        screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting_for_start = False
                break

        await asyncio.sleep(1 / 60)

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
        player.movePlayer()
        player.checkCollisions()
        player.powerUp()
        player.checkGhostCollisions()

        check_level_complete()

        # Move all ghosts
        for ghost in ghosts:
            ghost.turns_allowed = ghost.checkTurns()
            if counter % (4 + ghost.character) == 0:  # Different timing for each ghost
                ghost.findPath(player.readRow(), player.readCol())
            ghost.moveGhost()

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

        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())
pygame.quit()