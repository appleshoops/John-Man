from typing import override
from object import Object
import pygame
import math
import game

class Player(Object): # player is a subclass of object from game.py
    def __init__(self, surface, row, col, xPos, yPos, direction, player_images, sprite=None):
        super().__init__(surface, row, col, xPos, yPos)
        self.direction = 0
        self.player_images = player_images

    @override
    def drawSprite(self):
        # the 4 directions john can face (0=R, 1=L, 2=U, 3=D)
        if self.direction == 0:
            screen.blit(self.player_images[counter // 5], (self.ReadXPos(), self.ReadYPos())) # cycle the john man frames on a timer
        elif self.direction == 1:
            screen.blit(pygame.transform.flip(self.player_images[counter // 5], True, False,) (self.ReadXPos(), self.ReadYPos())) # the pygame transform flip changes the direction of the sprite and the true/false tells it what axis to flip
        elif self.direction == 2:
            screen.blit(pygame.transform.rotate(self.player_images[counter // 5], 90), (self.ReadXPos(), self.ReadYPos())) # this time it uses rotate instead of flip because its easier
        elif self.direction == 3:
            screen.blit(pygame.transform.rotate(self.player_images[counter // 5], 270), (self.ReadXPos(), self.ReadYPos())) # and 270 degrees for down