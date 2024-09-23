import pygame
from variables import *
from bullet import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, t800, groups):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.screen = screen
        self.t800 = t800
        self.groups = groups
        self.direction = True # True = Right, False = Left
        self.patrol_area = 0
        self.visual_field = 200
        self.idle = True
        self.cooldown = 40
        self.health = 3
        self.recharging = False

        self.rect = pygame.Rect(x, y, CHARACTER_WIDTH, CHARACTER_HEIGHT)

    def update(self, level):
        self.level_map = level
        self.move()

        bullet_count = 0
        current_rect = pygame.Rect(self.rect.x - self.t800.scrolled ,self.rect.y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        bullet_group = self.groups[3]

        for bullet in bullet_group:
            bullet_count += 1
            if pygame.Rect.colliderect(current_rect, bullet.rect):
                bullet.kill()
                self.health -= 1
                self.t800.score += 5
        
        if self.health == 0:
            self.t800.score += 10
            self.kill()

        self.draw()

        if self.recharging and self.cooldown <= 40 and self.cooldown > 0:
            self.cooldown -= 1
        else:
            self.cooldown = 40
            self.recharging = False

    def move(self):
        obstacle_list = []
        delta_y = 0
        delta_x = 0

        if self.direction == True and self.patrol_area < 350 and self.idle:
            delta_x += SPEED / 2
            self.patrol_area += SPEED / 2
        elif self.patrol_area >= 350:
            self.direction = False

        if self.direction == False and self.patrol_area > 0 and self.idle:
            delta_x -= SPEED / 2
            self.patrol_area -= SPEED / 2
        elif self.patrol_area == 0:
            self.direction = True

        self.rect.x += delta_x

        for y, row in enumerate(range(12)):
          for x, tile in enumerate(range(48)):
                if self.level_map[y][x] == "1":
                    obstacle_tile = pygame.Rect(((x * TILE_SIZE) - self.t800.scrolled, y * TILE_SIZE),(CHARACTER_WIDTH, CHARACTER_HEIGHT))
                    obstacle_list.append(obstacle_tile)
        
        for obstacle in obstacle_list:
            if obstacle.colliderect((self.rect.x, self.rect.y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)):
                self.rect.y -= 10 

        if self.direction:
            if self.t800.rect.colliderect(self.rect.x - self.t800.scrolled + self.visual_field + CHARACTER_WIDTH, self.rect.y, CHARACTER_WIDTH - self.visual_field, CHARACTER_HEIGHT) and self.t800.alive == True:
                self.idle = False
                if self.cooldown == 40:
                    current_x = self.rect.x - self.t800.scrolled
                    self.shoot(current_x)
                    self.recharging = True
            else:
                self.idle = True
        elif self.direction == False:
            if self.t800.rect.colliderect(self.rect.x - self.t800.scrolled - self.visual_field, self.rect.y, CHARACTER_WIDTH + self.visual_field, CHARACTER_HEIGHT) and self.t800.alive == True:
                self.idle = False
                if self.cooldown == 40:
                    current_x = self.rect.x - self.t800.scrolled
                    self.shoot(current_x)
                    self.recharging = True
            else:
                self.idle = True
    
    def draw(self):
        pygame.draw.rect(self.screen, "blue", ((self.rect.x - self.t800.scrolled, self.rect.y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)))

    def shoot(self, current_x):
        bullet = Bullet(current_x, self.rect.y, self.direction)
        enemy_bullet_group = self.groups[2]
        enemy_bullet_group.add(bullet)