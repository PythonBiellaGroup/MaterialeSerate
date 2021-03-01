# https://www.pygame.org/docs/ref/draw.html

import pygame
import sys
import time

# init the library 
pygame.init()

# init the window
size = (500, 500)
screen = pygame.display.set_mode(size)

# set the caption
pygame.display.set_caption(sys.argv[0])

# fill screen 
screen.fill((255,0,0))

# create a surface and draw a circle on it
surf = pygame.Surface((200, 200))
pygame.draw.circle(surf, (0, 0, 255), (0,0), 150)

# blit and update
screen.blit(surf, (100, 100))
pygame.display.flip()

# delay 2 sec
time.sleep(2)

# Close the window and quit.
pygame.quit()