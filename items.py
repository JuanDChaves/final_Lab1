import pygame
from variables import *

class Transition_Item(pygame.sprite.Sprite):
    def __init__(self, x , y, type):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.type = type

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, type, coordinates):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.type = type
        self.coordinates = coordinates