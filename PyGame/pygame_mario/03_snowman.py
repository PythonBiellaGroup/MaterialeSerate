"""
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/_XdrKSDmzqA

"""

# Import a library of functions called 'pygame'
import pygame


def draw_snowman(screen, x, y):
    """ --- Function for a snowman ---
    Define a function that will draw a snowman at a certain location.
    """
    pygame.draw.ellipse(screen, WHITE, [35 + x, 0 + y, 25, 25])
    pygame.draw.ellipse(screen, WHITE, [23 + x, 20 + y, 50, 50])
    pygame.draw.ellipse(screen, WHITE, [0 + x, 65 + y, 100, 100])


# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

# Set the height and width of the screen
size = [400, 500]
screen = pygame.display.set_mode(size)

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear the screen and set the screen background
    screen.fill(BLACK)

    # Snowman in upper left
    draw_snowman(screen, 10, 10)

    # Snowman in upper right
    draw_snowman(screen, 300, 10)

    # Snowman in lower left
    draw_snowman(screen, 10, 300)

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)


# Be IDLE friendly
pygame.quit()
