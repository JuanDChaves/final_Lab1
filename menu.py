import pygame
import json
from variables import *
from button import *

class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.btn_id = "main"
        self.clicked = False

    # DESDE AQUI SE ABRE EL ARCHIVO CON LA INFO DE LOS BTONES DEL MENU
        self.main_menu_coords = {"play": (50, 50), "settings": (400, 50), "levels": (50, 200), "scores": (400, 200), "about": (50, 400), "quit": (400, 400)}
        self.retry_menu_coords = {"play": (50, 50), "main": (400, 50)}
        self.settings_menu_coords = {"main": (50, 50)} 
        self.levels_menu_coords = {"main": (50, 50)}
        self.scores_menu_coords = {"main": (50, 50)}
        self.about_menu_coords = {"main": (50, 50)}
    
    def show(self):
        if self.btn_id == "main":
            for key, value in self.main_menu_coords.items():
                self.btn_manager(key, value)
        elif self.btn_id == "retry":
            for key, value in self.retry_menu_coords.items():
                self.btn_manager(key, value)
        elif self.btn_id == "settings":
            for key, value in self.settings_menu_coords.items():
                self.btn_manager(key, value)
        elif self.btn_id == "levels":
            for key, value in self.levels_menu_coords.items():
                self.btn_manager(key, value)
        elif self.btn_id == "scores":
            for key, value in self.scores_menu_coords.items():
                self.btn_manager(key, value)
        elif self.btn_id == "about":
            for key, value in self.about_menu_coords.items():
                self.btn_manager(key, value)

    def btn_manager(self, key, value):
        button = Button(value[0], value[1])
        button.draw(self.screen)
        self.pos = pygame.mouse.get_pos()
        current_rect = pygame.Rect((value[0], value[1]),(BTN_WIDTH, BTN_HEIGHT))
        if pygame.Rect.collidepoint(current_rect, self.pos):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.btn_id = key
                    self.clicked = True
                
    def get_clicked_btn(self):
        return self.btn_id