# https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
# https://www.pygame.org/docs/ref/rect.html

import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, game, color, size, position=(0, 0)):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self._game = game

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface(size)
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect(topleft=position)
    
    def update(self):
        self.rect.x = self._game.m_position[0]
        self.rect.y = self._game.m_position[1]


class Game():

    def __init__(self):
        self._running = True
        self._size = (1000, 1000)
        self.screen = pygame.display.set_mode(self._size)
        self._clock = pygame.time.Clock()
        self._user = Block(self, WHITE, (50, 50))
        self.m_position = (0, 0)
        self._all = pygame.sprite.Group()
        self._group = pygame.sprite.Group()
        self._user_group = pygame.sprite.GroupSingle()
        self._user_group.add(self._user)
        self._all.add(self._user)

        for x in range(0, 20):
            size = (30, 30)
            position = (random.randint(0 + size[0], self._size[0] - size[0]),
                        random.randint(0 + size[1], self._size[1] - size[1]))
            print(position)
            block = Block(self, WHITE, size, position=position)
            self._group.add(block)
            self._all.add(block)
            
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
            self._user_group.update()

            pygame.sprite.groupcollide(self._user_group, self._group, False, True)
    
            self._all.draw(self.screen)
            print(len(self._group.sprites()))
            
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