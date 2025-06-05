import pygame
import math

TILEWIDTH = 28
TILEHEIGHT = 28

class Object:   # create object class that works as a parent class for all the objects drawn onto the screen at launch
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

    def drawSprite(self):   # draws sprite onto the object
        if self.__sprite:
            # Calculate the center position of the tile
            sprite_width = self.__sprite.get_width()
            sprite_height = self.__sprite.get_height()
            center_x = self.__xPos + (TILEWIDTH - sprite_width) // 2
            center_y = self.__yPos + (TILEHEIGHT - sprite_height) // 2
            # Draw the sprite at the center of the tile
            self.__surface.blit(self.__sprite, (center_x, center_y))