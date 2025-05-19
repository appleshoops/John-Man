# importing the library
from this import d
from typing import override
import pygame
import random

class Shapes:   # Parent classs
    def __init__(self, surface, color, xPos, yPos):
        self.__surface = surface
        self.__color = color
        self.__xPos = xPos
        self.__yPos = yPos

    def ReadSurface(self):
        return self.__surface
    
    def ReadColor(self):
        return self.__color

    def SetXPos(self, moveValue):
        self.__xPos = moveValue

    def ReadXPos(self):
        # read the value of an attribute
        return self.__xPos
    
    def SetYPos(self, moveValue):
        self.__yPos = moveValue

    def ReadYPos(self):
        return self.__yPos

class DrawRect(Shapes):     # Inheriting from parent class
    def __init__(self, surface, color, xPos, yPos, width, height):
        super().__init__(surface, color, xPos, yPos)
        self.__width = width
        self.__height = height
        self.__movingLeft = self.SetDirection()
        self.__movingDown = self.SetDirection()
    
    def SetDirection(self):
        x = random.randint(0, 1)
        if x == 0:
            return True
        else:
            return False
        # __ means that the attribute is protected and cannot be directly accessed by another object

    def DrawShape(self):
        pygame.draw.rect(self.ReadSurface(), self.ReadColor(), [self.ReadXPos(), self.ReadYPos(), self.__width, self.__height], 0)
        # pygame.display.update()

    def SetXPos(self, moveValue):
        newPos = self.ReadXPos()
        if self.__movingLeft:   # if true
            if self.ReadXPos() <= 0:   # if shape is on or below boundary
                self.__movingLeft = False  # Changed == to =
            else:
                newPos = self.ReadXPos() - moveValue
        else:
            if self.ReadXPos() + self.__width >= screenWidth:
                self.__movingLeft = True
            else:
                newPos = self.ReadXPos() + moveValue
        super().SetXPos(newPos)  # Call parent method to update position

    def SetYPos(self, moveValue):
        newPos = self.ReadYPos()
        if self.__movingDown:
            if self.ReadYPos() + self.__height >= screenHeight:
                self.__movingDown = False
            else:
                newPos = self.ReadYPos() + moveValue
        else:
            if self.ReadYPos() <= 0:
                self.__movingDown = True
            else:
                newPos = self.ReadYPos() - moveValue
        super().SetYPos(newPos)

class DrawCircle(Shapes):   # Inheriting from parent class
    def __init__(self, surface, color, xPos, yPos, radius):
        super().__init__(surface, color, xPos, yPos)
        self.__radius = radius
        self.__movingUp = self.setDirection()
        self.__movingLeft = self.setDirection()
    
    def setDirection(self):
        y = random.randint(0, 1)
        if y == 0:
            return True
        else:
            return False

    def SetYPos(self, moveValue):
        newPos = self.ReadYPos()
        if self.__movingUp:
            if self.ReadYPos() - self.__radius <= 0:  # Check if hitting top boundary
                self.__movingUp = False
            else:
                newPos = self.ReadYPos() - moveValue
        else:
            if self.ReadYPos() + self.__radius >= screenHeight:  # Check if hitting bottom boundary
                self.__movingUp = True

                
            else:
                newPos = self.ReadYPos() + moveValue
        super().SetYPos(newPos)
    
    def SetXPos(self, moveValue):
        newPos = self.ReadXPos()
        if self.__movingLeft:   # if true
            if self.ReadXPos() <= 0:   # if shape is on or below boundary
                self.__movingLeft - self.__radius == False  # Changed == to =
            else:
                newPos = self.ReadXPos() - moveValue
        else:
            if self.ReadXPos() + self.__radius >= screenWidth:
                self.__movingLeft = True
            else:
                newPos = self.ReadXPos() + moveValue
        super().SetXPos(newPos)  # Call parent method to update position

    def DrawShape(self):
        pygame.draw.circle(self.ReadSurface(), self.ReadColor(), [self.ReadXPos(), self.ReadYPos()], self.__radius, 0)

def DrawShapes(shapeList):
    for shape in shapeList:
        shape.DrawShape()

def MoveShapes(shapeList, moveValue):
    for shape in shapeList:
        shape.SetXPos(moveValue)
        shape.SetYPos(moveValue)
        # shape.__yPos += moveValue
        


# initializing all the importe
# pygame modules
(numpass,numfail) = pygame.init()
 
# printing the number of modules 
# initialized successfully
print('Number of modules initialized successfully:', numpass)

# displaying a window of height 
# resolution of the window
screenWidth = 1280
screenHeight = 720 
pygame.display.set_mode((screenWidth, screenHeight))

# Initializing RGB Color
bgColor = (0, 0, 0)

# Creating a reference to the surface
surface = pygame.display.get_surface()

# Changing surface color
surface.fill(bgColor)  # setting acolor for the background
pygame.display.flip()  # render the bgcolor

# set title in the title bar
title = 'Intro to pygame'
pygame.display.set_caption(title) 

# instantiate objects from the DrawRect class
# rect1 = DrawRect(surface, (0, 0, 255), 100, 100, 400, 100)
# rect2 = DrawRect(surface, (0, 255, 0), screenWidth, screenHeight, 200, 50)
shapeList = []  # store out rect objects
for i in range(5):
    col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    sizeX = random.randint(1,250)
    sizeY = random.randint(1,250)
    posX = random.randint(0, screenWidth - sizeX)
    posY = random.randint(0, screenHeight - sizeY)
    shapeList.append(DrawRect(surface, col, posX, posY, sizeX, sizeY))
    # print(rectList[i].ReadXPos())

for i in range(5):
    col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    rad = random.randint(1, 100)
    posX = random.randint(0, screenWidth - sizeX)
    posY = random.randint(0, screenWidth - sizeY)

    shapeList.append(DrawCircle(surface, col, posX, posY, rad))

# creating a bool value which checks allows the game to run
running = True
  
# keep game running till running is true (run the game loop while true)
while running: 
    
    # Check for event if user has pushed any event in queue 
    for event in pygame.event.get(): 
          
        # if event is of type quit then set running bool to false 
        if event.type == pygame.QUIT: 
            running = False
    
    # Changing surface color
    surface.fill(bgColor)  # setting acolor for the background

    # Using draw.rect module of
    # pygame to draw the outlined rectangle
    # (what we draw on, color of shape, size and position of shape, width of outline)
    # pygame.draw.rect(surface, (0, 0, 255), [100, 100, 400, 100], 0)
    # rect1.DrawShape()
    # rect2.DrawShape()
    DrawShapes(shapeList)
    MoveShapes(shapeList, 1)

    #pygame.display.flip()  # render the bgcolor
    pygame.display.update()  # update the display
