import pygame

class Player():
    def __init__(self, surface, sprite, xPos, yPos):
        self.__surface = surface
        self.__sprite = sprite
        self.__xPos = xPos
        self.__yPos = yPos
        self.__speed = 5
    
    def Movement(self, keysPressed):
        if keysPressed[pygame.K_UP] or keysPressed[pygame.K_w]:
            self.__yPos -= self.__speed
        elif keysPressed[pygame.K_DOWN] or keysPressed[pygame.K_s]:
            self.__yPos += self.__speed
    
        if keysPressed[pygame.K_RIGHT] or keysPressed[pygame.K_d]:
            self.__xPos += self.__speed
        elif keysPressed[pygame.K_LEFT] or keysPressed[pygame.K_a]:
            self.__xPos -= self.__speed
    
    def getXPos(self):
        return(self.__xPos)

    def getYPos(self):
        return(self.__yPos)

    def getPos(self):
        return (self.__xPos, self.__yPos)

    def drawSprite(self):
        self.__surface.blit(self.__sprite, (self.__xPos, self.__yPos),)


# initializing all imported pygame modules
(numpass, numfail) = pygame.init()

# printing the number of modules initialized successfully and failed
print("number of modules initialized successfully:", numpass)

# displaying a window of height 480 and width 640
screenWidth = 1280
screenHeight = 720
surface = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)

# initialize the color
BGcolor = (230, 137, 170)

clock = pygame.time.Clock()
cSpeed = 60
# set a reference to the clock speed

# set title of the window
title = "jake wu man"
pygame.display.set_caption(title)

player = pygame.Rect(150, 150, 50, 50)
# creating a surface object
playerSprite = pygame.image.load("Intro/sprites/player.png").convert_alpha()
# Remove this line or use it for something else
# playerSpriteLocation = "Intro/sprites/player.png"

# Pass the actual Surface object, not the string path
player = Player(surface, playerSprite, screenWidth/2, screenHeight/2)

def Draw():
    surface.fill(BGcolor)
    # pygame.display.flip()
    # pygame.draw.rect(surface, (110, 189, 193), player)
    player.drawSprite()



# creating a bool value which checks if the game is running or not
running = True

# keep game running till running is true (run the game loop while true)
while running:
    # check for event if user has pushed any event in queue
    for event in pygame.event.get():
        # if user has clicked on the cross button of the window
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
    player.Movement(keys)  # Add this line to handle movement

    print(player.getXPos())  # Add parentheses to call the method
    Draw()
    pygame.display.update()
#    clock.tick(cSpeed)
