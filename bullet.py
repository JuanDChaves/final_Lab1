import pygame
from variables import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,20))
        self.image.fill("white")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        if self.direction:
            self.rect.x += 8
        else:
            self.rect.x -= 8

        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH:
            self.kill()