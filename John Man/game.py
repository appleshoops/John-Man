# imports
import pygame
from pygame.locals import *
import math

# create constant variables
TILEWIDTH = 16
TILEHEIGHT = 16
NUMBERROWS = 36
NUMBERCOLS = 28
SCREENWIDTH = TILEWIDTH * NUMBERCOLS
SCREENHEIGHT = TILEHEIGHT * NUMBERROWS
BLACK = (0, 0, 0)

class GameController(obejct):
    def __init__(self):
        pygame.init()