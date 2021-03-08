# https://www.pygame.org/docs/ref/sprite.html
# https://www.pygame.org/docs/ref/rect.html

import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, game, color, size):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self._game = game

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface(size)
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
    
    def display_rect(self):

        pygame.draw.rect(self._game.screen, (255, 0, 0),
                         self.rect, 1)

    def update(self):
        # self.rect.x = self._game.m_position[0]
        # self.rect.y = self._game.m_position[1]
        self._game.screen.blit(self.image, self._game.m_position)
        # self.display_rect() 


class Game():

    def __init__(self):
        self._running = True
        self._size = (1000, 1000)
        self.screen = pygame.display.set_mode(self._size)
        self._clock = pygame.time.Clock()
        self._sprite = Block(self, WHITE, (30, 30))
        self.m_position = (0, 0)

    def run(self):
        # main loop
        while self._running:
            # fill screen 
            self.screen.fill(BLACK)

            # handling events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.MOUSEMOTION:
                    self.m_position = pygame.mouse.get_pos()
            
            # update sprite
            self._sprite.update()
            
            # clock cap 60 ticks per seconds
            self._clock.tick(60)
            # clock.get_fps()
            
            # update
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()