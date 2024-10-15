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
        self.asset_images = []
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
                if self.level_map[y][x] == "88":
                    lava_item = Transition_Item((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE, "lava")
                    self.transition_item_group.add(lava_item)
                elif self.level_map[y][x] == "90":
                    health_item = Item((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE, "health", (y, x))
                    self.item_group.add(health_item)
                elif self.level_map[y][x] == "82":
                    ammo_item = Item((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE, "ammo", (y, x))
                    self.item_group.add(ammo_item)
                elif self.level_map[y][x] == "89":
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

    def load_assets(self):
        for i in range(1, 95):
            if i <= 87:
                asset_image = pygame.image.load(f"./images/tiles/{i}.png").convert_alpha()
                asset_image = pygame.transform.scale_by(asset_image, 1.6)
                self.asset_images.append(asset_image)
            elif i == 88 or i == 89:
                asset_image = pygame.image.load(f"./images/tiles/{i}.png").convert_alpha()
                asset_image = pygame.transform.scale_by(asset_image, 1.1)
                self.asset_images.append(asset_image)
            elif i == 90:
                asset_image = pygame.image.load(f"./images/tiles/{i}.png").convert_alpha()
                asset_image = pygame.transform.scale_by(asset_image, 2)
                self.asset_images.append(asset_image)
            else:
                asset_image = pygame.image.load(f"./images/tiles/{i}.png").convert_alpha()
                self.asset_images.append(asset_image)

        # 1-81, box, bench, fences, small * 1.6
        # 82 box
        # 83 bench
        # 84 - 86 fences
        # 87 small
        # 88 lava
        # 89 flag
        # 90 barrel
        # 91 big
        # 92 cryo
        # 93 hang
        # 94 server
        # lava, flag * 1.1
        # barrel * 2
        # big, cryo, hang, server 
        # Flag, server, small y - 20

    def draw(self):
        self.load_assets()
        for y, row in enumerate(range(MAP_HEIGHT)):
            for x, tile in enumerate(range(MAP_LENGTH)):
                tile_id = int(self.level_map[y][x])
                if tile_id == 0:
                    pass
                elif tile_id == 87 or tile_id == 89 or tile_id == 94: 
                    self.screen.blit(self.asset_images[tile_id - 1], ((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE - 20))
                else:
                    self.screen.blit(self.asset_images[tile_id - 1], ((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE))

    def enemies_1(self):
        coord_enemies = [(8,19), (8,40)]
        return coord_enemies

    def enemies_2(self):
        coord_enemies = [(8,23), (8,40)]
        return coord_enemies

    def enemies_3(self):
        coord_enemies = [(8,19), (8, 22), (8, 39), (8,43)]
        return coord_enemies