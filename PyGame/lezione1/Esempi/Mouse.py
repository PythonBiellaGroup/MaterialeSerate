# https://www.pygame.org/docs/ref/font.html#pygame.font.Font.render
# https://www.pygame.org/docs/ref/event.html
# https://www.pygame.org/docs/ref/mouse.html

import pygame
import sys
import time

# init the library 
pygame.init()

# init the window
size = (1000, 1000)
screen = pygame.display.set_mode(size)

# set the caption
pygame.display.set_caption(sys.argv[0])

# set game clock
clock = pygame.time.Clock()

running = True
pos_call = (0, 0)
pos_even = (0, 0)
font = pygame.font.SysFont("monospace", 25)

# main loop
while running:
    # fill screen 
    screen.fill((0,0,0))

    # handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            pos_call = pygame.mouse.get_pos()
            pos_even = event.pos

    string = font.render("     pos_call = " + str(pos_call) +
                         "pos_even = " + str(pos_even),
                         1, (255, 255, 255))
    screen.blit(string, pos_call)
    
    # clock cap 60 ticks per seconds
    clock.tick(60)
    # clock.get_fps()
    
    # update
    pygame.display.flip()



# Close the window and quit.
pygame.quit()