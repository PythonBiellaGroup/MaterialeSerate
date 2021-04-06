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
        self.rect = self.image.get_rect(center=position)
        self._position = position
        self._size = self.image.get_size()
        self._follow = False
    
    def update(self):
        size = self._game.get_screen_size()

        if self._follow:
            # user char handling with camera position
            self._game.set_camera([int(x) for x in self._position])

            x = (size[0] / 2.0) - self._size[0] / 2
            y = (size[1] / 2.0) - self._size[1] / 2

            # blitting
            self._game.screen.blit(self.image, (x, y))

        else:
            camera = self._game.get_camera()

            # calculate the center of the image
            centre = (self._position[0] - self._size[0] / 2,
                      self._position[1] - self._size[1] / 2)

            # blitting
            self._game.screen.blit(self.image, 
                                   [(size[0] / 2) - ((camera[0] - centre[0])),
                                    (size[1] / 2) - ((camera[1] - centre[1]))])


class Character(Game_object):

    def __init__(self, game, asset, position=(0.0, 0.0)):
        self._image_set = asset
        super().__init__(game, self._image_set[0], position)
        self._age = 0
        self._direction = 0
        self._asset_size = len(self._image_set)
        self._direction = 0
        self._moving = 0
        self.rect = self.image.get_rect(center=position)
        self._follow = True
        self._max_speed = 180

    def flipMe(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self._moving = 1
            self._direction = 1
        elif keys[pygame.K_a]:
            self._moving = 1
            self._direction = -1
        else:
            self._moving = 0

    def update(self):
        self.controls()

        if self._moving:
            self._age += self._asset_size * self._game.delta_time / 1000
            self._age %= self._asset_size
            self._position[0] += self._max_speed * self._direction * self._game.delta_time / 1000.0
            
        else:
            self._age = 0
        
        self.image = self._image_set[math.floor(self._age)]

        if self._direction == -1:
            self.flipMe()

        super().update()


class Game():

    def __init__(self):
        self._running = True
        self._size = (1920, 1080)
        self._center = list(x/2 for x in self._size)
        self.screen = pygame.display.set_mode(self._size)
        self._clock = pygame.time.Clock()
        self.delta_time = 0.0
        self._camera_position = [0, 0]
        self._all = pygame.sprite.Group()

        # loading assets
        redhat_run = "./redhat/run/"
        self._char_asset = [pygame.transform.smoothscale(pygame.image.load(redhat_run + x), [t//10 for t in self._size])
                            for x in sorted(os.listdir(redhat_run))]

        self._bg = pygame.transform.smoothscale(pygame.image.load("freetileset/png/BG/BG.png"), self._size)
        self.build_map()
        
        self._char = Character(self, self._char_asset, position= self._center)
        self._all.add(self._char)
    
    def get_camera(self):
        return self._camera_position

    def set_camera(self, position):
        self._camera_position = position

    def get_screen_size(self):
        return self._size

    def build_map(self):
        image = pygame.image.load("./freetileset/png/Object/Tree_3.png")
        tree = Game_object(self, image, [300, 300])
        self._all.add(tree)

    def run(self):
        # main loop
        while self._running:
            # clock cap 60 ticks per seconds
            self.delta_time = self._clock.tick(60)

            # fill screen 
            self.screen.fill(BLACK)
            self.screen.blit(self._bg, 
                                   ((self._size[0] / 2) - ((self._camera_position[0])),
                                    (self._size[1] / 2) - ((self._camera_position[1]))))
            # handling events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            # update sprite
            self._all.update()
            
            # flip
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()