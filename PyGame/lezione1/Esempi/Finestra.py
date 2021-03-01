# https://www.pygame.org/docs/ref/display.html

import pygame
import sys
import time

# init the library 
pygame.init()
# pygame.init() initializes the display too

# init the window
size = (int(sys.argv[1]), int(sys.argv[2]))
screen = pygame.display.set_mode(size)

# set the caption
pygame.display.set_caption(sys.argv[0])

# delay 2 sec
time.sleep(2)

# Close the window and quit.
pygame.quit()