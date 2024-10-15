import pygame
from variables import *

class Button():
    def __init__(self, key, x, y) -> None:
        self.key = key
        self.x = x 
        self.y = y
        self.btn = pygame.image.load(f"./images/buttons/{self.key}_btn.png").convert_alpha()
        self.btn = pygame.transform.scale_by(self.btn, 0.6)
    
    def draw(self, screen):
        self.screen = screen
        self.screen.blit(self.btn, (self.x, self.y))

    def get_size(self):
        return (self.btn.get_size())