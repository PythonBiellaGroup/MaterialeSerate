import pygame
import random
import math
import os

BLACK = (0, 0, 0)


class Game_object(pygame.sprite.Sprite):

    def __init__(self, game, image, position=(0.0, 0.0)):
        super().__init__()
        self._game = game
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self._position = position
    

class Character(Game_object):

    def __init__(self, game, asset, position=(0.0, 0.0)):
        self._image_set = asset
        super().__init__(game, self._image_set[0], position)
        self._age = 0
        self._direction = 0
        self._asset_size = len(self._image_set)
        self.direction = 0
        self.moving = 0
        self.rect = self.image.get_rect(center=position)
        print(self._asset_size)

    def flipMe(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        if self.moving:
            self._age += self._asset_size * self._game.delta_time / 1000
            self._age %= self._asset_size
        else:
            self._age = 0
        
        self.image = self._image_set[math.floor(self._age)]

        if not self.direction:
            self.flipMe()


class Game():

    def __init__(self):
        self._running = True
        self._size = (1000, 1000)
        self._center = list(x/2 for x in self._size)
        self.screen = pygame.display.set_mode(self._size)
        self._clock = pygame.time.Clock()
        self.delta_time = 0.0
        self._all = pygame.sprite.Group()

        self._asset = [pygame.image.load("./redhat/run/%s" % x) for x in sorted(os.listdir("./redhat/run"))]

        self._char = Character(self, self._asset, position= self._center)
        self._all.add(self._char)
            
    def run(self):
        # main loop
        while self._running:
            # clock cap 60 ticks per seconds
            self.delta_time = self._clock.tick(60)

            # fill screen 
            self.screen.fill(BLACK)

            # handling events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self._char.moving = 1
                        self._char.direction = 1
                    if event.key == pygame.K_a:
                        self._char.moving = 1
                        self._char.direction = 0

                if event.type == pygame.KEYUP:
                    self._char.moving = 0

            # update sprite
            self._all.update()
            self._all.draw(self.screen)

            # flip
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()