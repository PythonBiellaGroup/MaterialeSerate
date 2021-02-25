"""
 Animating multiple objects using a list.
 Inspired from: http://programarcadegames.com/
 Explanation video: http://youtu.be/Gkhz3FuhGoI
"""
# Import a library of functions called 'pygame'
import pygame
import random

# Initialize the game engine
pygame.init()

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

# Set the height and width of the screen
SIZE_X = 800
SIZE_Y = 800
SIZE = [SIZE_X, SIZE_Y]

# Numer of snow flakes
SNOW_FLAKES = 100

# Frames per seconds
FPS = 20

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Snow Animation")

# Create an empty array
snow_list = []

# Loop 50 times and add a snow flake as a random x,y position
for i in range(SNOW_FLAKES):
    x = random.randrange(0, SIZE_X)
    y = random.randrange(0, SIZE_Y)
    snow_list.append([x, y])

clock = pygame.time.Clock()

# Loop until the user clicks the close button.
done = False
while not done:

    for event in pygame.event.get():   # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True   # Flag that we are done so we exit this loop

    # Set the screen background
    screen.fill(BLACK)

    # Process each snow flake in the list
    for i in range(len(snow_list)):

        # Draw the snow flake
        pygame.draw.circle(screen, WHITE, snow_list[i], 2)

        # Move the snow flake down one pixel: element i, y coordinates
        snow_list[i][1] += 1

        # If the snow flake has moved off the bottom of the screen
        if snow_list[i][1] > SIZE_Y:
            # Reset it just above the top
            y = random.randrange(-50, -10)
            snow_list[i][1] = y
            # Give it a new x position
            x = random.randrange(0, SIZE_X)
            snow_list[i][0] = x

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    clock.tick(FPS)

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
