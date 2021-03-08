# https://www.pygame.org/docs/ref/sprite.html
# https://www.pygame.org/docs/ref/rect.html

import pygame
import random
import math


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Game_object(pygame.sprite.Sprite):

    def __init__(self, game, image, position=(0.0, 0.0)):
        super().__init__()
        self._game = game
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self._position = position
    
    def distance_from(self, point):
        """Euclidean distance between point and self calculated according to its _position attribute.
        Arguments:
            point {tuple: float}

        Returns:
            float -- absolute distance"""

        return ((self._position[0] - point[0])**2 +
                (self._position[1] - point[1])**2)**0.5 


class Food(Game_object):

    def __init__(self, game, image, position=(0, 0)):
        super().__init__(game, image, position)


class Nest(Game_object):

    def __init__(self, game, image, position=(0, 0)):
        super().__init__(game, image, position)
        self.rect.center = position
        self._food = 0

    def gather_food(self, ant):
        self._food += ant.drop_food()

    def get_food(self):
        return self._food


class Ant(Game_object):

    def __init__(self, game, image, position=(0, 0)):
        super().__init__(game, image, position)
        self.rect.center = position
        self._food = 0
        self._max_speed = 100.0 # pixel per second
        self._target = None
        self._angle = 0.0
    
    def gather_food(self, amount):
        self._food += amount

    def drop_food(self):
        food = self._food
        self._food = 0
        return food

    def get_target(self):
        return self._target 

    def delete_target(self):
        self._target = None

    def go_home(self):
        self._target = self._game.nest
        self._angle = self.get_angle()

    def get_angle(self):
        """Find angle based on x, y componentes"""

        return math.atan2(self._position[1] - self._target._position[1],
                          -self._position[0] + self._target._position[0])

    def find_target(self):
        """Find the closest target"""

        target = None
        for obj in self._game._food_group.sprites():
            if not target:
                target = obj
            elif self.distance_from(obj._position) < self.distance_from(target._position):
                target = obj
        
        if target:
            self._target = target
            self._angle = self.get_angle()

    def chase(self):
        """Seek the chosen target if alive"""

        self._position[0] += self._max_speed * math.cos(self._angle) *  self._game.delta_time / 1000.0
        self._position[1] += self._max_speed * -math.sin(self._angle) *  self._game.delta_time / 1000.0

    def update(self):
        """update override"""
        
        if self._target and self._target.alive():
            self.chase()
            self.rect.center = self._position
        else:
            self.find_target()


class Game():

    def __init__(self):
        self._running = True
        self._size = (1000, 1000)
        self._center = list(x/2 for x in self._size)
        self.screen = pygame.display.set_mode(self._size)
        self._clock = pygame.time.Clock()
        self.delta_time = 0.0
        self._font = pygame.font.SysFont("monospace", 25)

        self._all = pygame.sprite.Group()
        self._ant_group = pygame.sprite.Group()
        self._food_group = pygame.sprite.Group()
        self._nest_group = pygame.sprite.GroupSingle()

        self._background = pygame.image.load("bg.jpg")
        self._nest_image = pygame.image.load("nest.png")
        self._ant_image = pygame.image.load("ant.png")
        #self._food_image = pygame.Surface((6, 6))
        #self._food_image.fill(RED)
        self._food_image = pygame.image.load("seed.png") 

        self.nest = Nest(self, self._nest_image, position=self._center)
        self._nest_group.add(self.nest)
        self._all.add(self.nest)

        # creating ants
        for x in range(0, 10):
            position = [random.randint(0, self._size[0]),
                        random.randint(0, self._size[1])]
            element = Ant(self, self._ant_image, position=position)

            self._ant_group.add(element)
            self._all.add(element)

        # creating food
        for x in range(0, 90):
            size = self._food_image.get_size()
            position = [random.randint(0 + size[0], self._size[0] - size[0]),
                        random.randint(0 + size[1], self._size[1] - size[1])]
            element = Food(self, self._food_image, position=position)

            self._food_group.add(element)
            self._all.add(element)
            
    def run(self):
        # main loop
        while self._running:
            # clock cap 60 ticks per seconds
            self.delta_time = self._clock.tick(60)
            fps = self._clock.get_fps()

            # fill screen 
            self.screen.blit(self._background, (0, 0))

            # handling events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
            
            # collisions with nest
            collisions = pygame.sprite.groupcollide(self._nest_group, self._ant_group, False, False)
            if collisions: 
                for ant in collisions[self.nest]:
                    self.nest.gather_food(ant)
                    if ant.get_target() == self.nest:
                        ant.delete_target()
            
            # food gathering
            collisions = pygame.sprite.groupcollide(self._ant_group, self._food_group, False, True)
            if collisions: 
                for ant in collisions:
                    amount = len(collisions[ant])
                    ant.gather_food(amount)
                    ant.go_home()

            # update sprite
            self._all.update()
            self._all.draw(self.screen)

            # info
            string = self._font.render("fps: " + "%.9f" % fps +
                                       "  score: " + str(self.nest.get_food()),
                                       1, RED)
            self.screen.blit(string, (0, 0))
            
            # flip
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()