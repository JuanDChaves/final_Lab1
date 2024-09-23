import pygame
from variables import *

class Button():
    def __init__(self, x, y) -> None:
        self.x = x 
        self.y = y
    
    def draw(self, screen):
        self.screen = screen
        pygame.draw.rect(self.screen, "white", ((self.x, self.y), (BTN_WIDTH, BTN_HEIGHT)))