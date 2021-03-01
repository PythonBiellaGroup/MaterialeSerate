# https://www.pygame.org/docs/ref/font.html#pygame.font.Font.render
# https://www.pygame.org/docs/ref/event.html
# https://www.pygame.org/docs/ref/key.html
# https://www.pygame.org/docs/ref/mixer.html

import pygame
import sys
import time

# pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)

# init the library 
pygame.init()
# Initializes the diaplay and the mixer too

# init the window
size = (1000, 1000)
screen = pygame.display.set_mode(size)


if not pygame.mixer.get_init():
    # if mixer is not ready, terminate the execution
    exit(1)

# start music on the music channel 
pygame.mixer.music.load("Chill Out Records - Winter Lights - After The Fall.ogg")
pygame.mixer.music.play(loops=-1)
# The difference between the music playback and regular Sound playback is that the music is streamed, and never actually loaded all at once.

# sounds
click = pygame.mixer.Sound("Click.ogg")

# set the caption
pygame.display.set_caption(sys.argv[0])

# set game clock
clock = pygame.time.Clock()

running = True
pos_call = (0, 0)
pos_even = (0, 0)
font = pygame.font.SysFont("monospace", 25)
surf0 = pygame.Surface((100, 100))
# create 'A' 
A = pygame.image.load('a.png')

# main loop
while running:
    # fill screen 
    screen.fill((0,0,0))

    # list of pressed letters
    keys = pygame.key.get_pressed()

    # handling events when they happen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print("letter " + str(event.key) + " aka '" + pygame.key.name(event.key) + "' down")
            click.play()
            # print(keys)
        if event.type == pygame.KEYUP:
            print("letter " + str(event.key) + " aka '" + pygame.key.name(event.key) + "' up")
    
    # clock cap 60 ticks per seconds
    clock.tick(60)
    # clock.get_fps()

    # checking at every Tick
    if keys[pygame.K_a]:
        screen.blit(A, (0, 0))
    
    # update
    pygame.display.flip()



# Close the window and quit.
pygame.quit()