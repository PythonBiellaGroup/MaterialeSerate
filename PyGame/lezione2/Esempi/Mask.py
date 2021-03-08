# https://www.pygame.org/docs/ref/sprite.html
# https://www.pygame.org/docs/ref/rect.html

import pygame
import random


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Game_object(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, game, image, position=(0, 0)):
       # Call the parent class (Sprite) constructor
        super().__init__()

        self._game = game

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = image

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect(topleft=position)


class Ship(Game_object):

    def update(self):
        self.rect.x = self._game.m_position[0]
        self.rect.y = self._game.m_position[1]


class Asteroid(Game_object):

    def __init__(self, game, image, position=(0, 0)):
        super().__init__(game, image, position)


class Game():

    def __init__(self):
        self._running = True
        self._size = (1000, 1000)
        self.screen = pygame.display.set_mode(self._size)
        self._clock = pygame.time.Clock()
        self._ship_image = pygame.image.load("ship.png")
        self._user = Ship(self, self._ship_image)
        self.m_position = (0, 0)
        self._all = pygame.sprite.Group()
        self._asteroids = pygame.sprite.Group()
        self._user_group = pygame.sprite.GroupSingle()
        self._user_group.add(self._user)
        self._all.add(self._user)
        self._asteroid_image = pygame.image.load("asteroid.png")

        for x in range(0, 20):
            size = self._asteroid_image.get_size()
            position = (random.randint(0 + size[0], self._size[0] - size[0]),
                        random.randint(0 + size[1], self._size[1] - size[1]))
            block = Asteroid(self, self._asteroid_image, position=position)
            self._asteroids.add(block)
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

            collisions = pygame.sprite.groupcollide(self._user_group, self._asteroids, False, False)
            if collisions: 
                for x in collisions[self._user]:
                    if pygame.sprite.collide_mask(self._user, x):
                        x.kill()
    
            self._all.draw(self.screen)
            print(len(self._asteroids.sprites()))
            
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