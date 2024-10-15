import pygame
import json
from variables import *
from button import *

class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.btn_id = "main"
        self.clicked = False
        with open("./jsonConfig/buttons.json") as file:
            self.buttons = json.load(file)

    def show(self, btn_id):
        self.btn_id = btn_id
        for key, value in self.buttons[self.btn_id].items():
            self.btn_manager(key, value)

    def btn_manager(self, key, value):
        button = Button(key, value[0], value[1])
        button.draw(self.screen)
        button_size = button.get_size()
        self.pos = pygame.mouse.get_pos()
        current_rect = pygame.Rect((value[0] + 10, value[1] + 10), (button_size[0] - 20, button_size[1] - 20))
        if pygame.Rect.collidepoint(current_rect, self.pos):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.btn_id = key
                    self.clicked = True
                
    def get_clicked_btn(self):
        return self.btn_id