# https://www.pygame.org/docs/ref/image.html
# https://www.pygame.org/docs/ref/surface.html

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
screen.fill((0,0,0))

# create a surface
surf = pygame.image.load('asteroid.png')

# blit and update
screen.blit(surf, (0, 0))
pygame.display.flip()

# delay 2 sec
time.sleep(3)

# Close the window and quit.
pygame.quit()