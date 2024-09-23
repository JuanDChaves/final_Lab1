import pygame
import json
from variables import *
from items import *

class Map():
    def __init__(self, screen, t800, level, groups) -> None:
        self.screen = screen
        self.t800 = t800
        self.level = level
        self.level_map = []
        self.item_group = groups[0]
        self.transition_item_group = groups[1]
        with open("./jsonConfig/maps.json") as file:
            self.maps = json.load(file)

    def process(self):
        self.level_map.clear()
        if self.level == 1:
            self.level_map = self.maps["level1"]
        elif self.level == 2:
            self.level_map = self.maps["level2"]
        elif self.level == 3:
            self.level_map = self.maps["level3"]

        for y, row in enumerate(range(MAP_HEIGHT)):
            for x, tile in enumerate(range(MAP_LENGTH)):
                if self.level_map[y][x] == "2":
                    lava_item = Transition_Item((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE, "lava")
                    self.transition_item_group.add(lava_item)
                elif self.level_map[y][x] == "3":
                    health_item = Item((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE, "health", (y, x))
                    self.item_group.add(health_item)
                elif self.level_map[y][x] == "4":
                    ammo_item = Item((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE, "ammo", (y, x))
                    self.item_group.add(ammo_item)
                elif self.level_map[y][x] == "8":
                    exit_item = Transition_Item((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE, "exit")
                    self.transition_item_group.add(exit_item)
        return self.level_map

    def update(self):
        for item in self.item_group:
            item_rect = pygame.Rect((item.x - self.t800.scrolled, item.y),(TILE_SIZE, TILE_SIZE))
            if self.t800.rect.colliderect(item_rect):
                if item.type == "health":
                    self.t800.health += 10
                    self.level_map[item.coordinates[0]][item.coordinates[1]] = "0"
                    item.kill()
                if item.type == "ammo":
                    self.t800.ammonition += 10
                    self.level_map[item.coordinates[0]][item.coordinates[1]] = "0"
                    item.kill()

        for item in self.transition_item_group:
            item_rect = pygame.Rect((item.x - self.t800.scrolled + 20, item.y), (TILE_SIZE, TILE_SIZE))
            if self.t800.rect.colliderect(item_rect):
                if item.type == "lava":
                    self.t800.lost = True
                if item.type == "exit":
                    self.t800.score += 10
                    self.t800.won = True

    def draw(self):
        for y, row in enumerate(range(MAP_HEIGHT)):
            for x, tile in enumerate(range(MAP_LENGTH)):
                # 1 Block = saddlebrown
                # 2 lava = organgered
                # 3 Health = crimson
                # 4 Ammo = silver
                # 5 Deco1 = paleturquoise
                # 6 Deco2 = papayawhip
                # 7 Deco3 = palegreen
                # 8 Exit = gold
                # T800 = blue
                # T1000 = black
                if self.level_map[y][x] == "1":
                    pygame.draw.rect(self.screen, "saddlebrown", (((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
                elif self.level_map[y][x] == "2":
                    pygame.draw.rect(self.screen, "orangered", (((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
                elif self.level_map[y][x] == "3":
                    pygame.draw.rect(self.screen, "crimson", (((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
                elif self.level_map[y][x] == "4":
                    pygame.draw.rect(self.screen, "silver", (((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
                elif self.level_map[y][x] == "5":
                    pygame.draw.rect(self.screen, "paleturquoise", (((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
                elif self.level_map[y][x] == "6":
                    pygame.draw.rect(self.screen, "papayawhip", (((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
                elif self.level_map[y][x] == "7":
                    pygame.draw.rect(self.screen, "palegreen", (((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
                elif self.level_map[y][x] == "8":
                    pygame.draw.rect(self.screen, "gold", (((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
                elif self.level_map[y][x] == "9":
                    pygame.draw.rect(self.screen, "orangered", (((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))

    def enemies_1(self):
        coord_enemies = [(8,19), (8,40)]
        return coord_enemies