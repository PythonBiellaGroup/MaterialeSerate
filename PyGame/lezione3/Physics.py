import pygame
import random
import math
import os

BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Game_object(pygame.sprite.Sprite):

    def __init__(self, game, image, position=(0.0, 0.0)):
        super().__init__()
        self._game = game
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self._position = position
        self._size = self.image.get_size()
        self._follow = False
        self._gravity = 400.0 # pixel /s /s
        self._vertical_speed = 0.0
        self._max_vSpeed = 1000.0
        self._static = True
    
    def update_rect(self):
        self.rect.centerx = int(self._position[0])
        self.rect.centery = int(self._position[1])

    def display_rect(self):
        size = self._game.get_screen_size()
        camera = self._game.get_camera()
        new_rect = self.rect.copy()

        # calculate the center of the image
        centre = (self._position[0] - self._size[0] / 2,
                    self._position[1] - self._size[1] / 2)
        location = [(size[0] / 2) - ((camera[0] - centre[0])),
                    (size[1] / 2) - ((camera[1] - centre[1]))]
        new_rect.topleft = location
        pygame.draw.rect(self._game.screen, (255, 0, 0),
                         new_rect, 1)

    def update(self):
        self.update_rect()
        size = self._game.get_screen_size()

        if not self._static:
            if self._vertical_speed < self._max_vSpeed:
                self._vertical_speed += self._gravity * self._game.delta_time 
            else:
                self._vertical_speed = self._max_vSpeed
        
        self._position[1] += self._vertical_speed * self._game.delta_time  

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
        self.display_rect()


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
        self._up = False
        #self._static = False

    def flipMe(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def jump(self):
        if self._vertical_speed == 0.0:
            self._vertical_speed = -300

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
        if self._vertical_speed < 0:
            self._up = True
        else:
            self._up = False

        if self._moving:
            self._age += self._asset_size * self._game.delta_time
            self._age %= self._asset_size
            self._position[0] += self._max_speed * self._direction * self._game.delta_time 
            
        else:
            self._age = 0
        
        self.image = self._image_set[math.floor(self._age)]

        if self._direction == -1:
            self.flipMe()
        
        caught = pygame.sprite.spritecollide(self, self._game._env, False)
        if not self._up and caught and caught[0].rect.bottom >= self.rect.top and caught[0].rect.top <= self.rect.bottom:
            self._static = True
            self._vertical_speed = 0.0
            self._position[1] = caught[0]._position[1] - caught[0]._size[1]/2 - self._size[1]/2 + 1
        else:
            self._static = False

        super().update()


class Game():

    def __init__(self):
        self._running = True
        self._size = (3000, 2000)
        self._center = list(x/2 for x in self._size)
        self.screen = pygame.display.set_mode(self._size)
        self._clock = pygame.time.Clock()
        self.delta_time = 0.0
        self._camera_position = [0, 0]
        self._all = pygame.sprite.Group()
        self._env = pygame.sprite.Group()
        self._font = pygame.font.SysFont("monospace", 25)

        # loading assets
        redhat_run = "./redhat/run/"
        self._char_asset = [pygame.transform.smoothscale(pygame.image.load(redhat_run + x).convert_alpha(), [t//10 for t in self._size])
                            for x in sorted(os.listdir(redhat_run))]

        tiles = "./freetileset/png/Tiles/"
        self._env_asset = [pygame.transform.smoothscale(pygame.image.load(tiles + x).convert_alpha(), [t//10 for t in self._size])
                           for x in sorted(os.listdir(tiles))]

        # remember to convert
        self._bg = pygame.transform.smoothscale(pygame.image.load("freetileset/png/BG/BG.png"), self._size).convert()
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
        size = image.get_size()
        tree = Game_object(self, image, [300, self._size[1] - size[1]/2-100])
        self._all.add(tree)

        for x in range(1, len(self._env_asset)):
            size = self._env_asset[x].get_size()
            tile = Game_object(self, self._env_asset[x], [0 + size[0] * x, self._size[1] - size[1]/2])
            self._env.add(tile)
            self._all.add(tile)


    def run(self):
        # main loop
        while self._running:
            # clock cap 60 ticks per seconds
            self.delta_time = self._clock.tick(60) / 1000.0

            fps = self._clock.get_fps()

            # fill screen 
            self.screen.fill(BLACK)
            self.screen.blit(self._bg, 
                                   (0, 0))
            # handling events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self._char.jump()

            # update sprite
            self._all.update()

            # info
            string = self._font.render("fps: " + "%.9f" % fps,
                                       1, RED)
            self.screen.blit(string, (0, 0))
           
            # flip
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
