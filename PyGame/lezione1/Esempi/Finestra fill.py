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

# fill the screen
screen.fill((255,0,0))
# refresh the screen
pygame.display.flip()
# pygame.display.update() allows better control 
# https://www.pygame.org/docs/ref/display.html#pygame.display.update

# delay 2 sec
time.sleep(2)

# Close the window and quit.
pygame.quit()