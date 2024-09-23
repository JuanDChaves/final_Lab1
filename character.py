import pygame
from variables import *
from bullet import *

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, groups):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.screen = screen
        self.groups = groups
        self.position = (x,y)
        self.vertical_speed = 0
        self.jumped = False
        self.jumping = False
        self.move_right = False
        self.move_left = False
        self.direction = True
        self.shooting = False
        self.alive = True
        self.ammonition = 10
        self.health = 5
        self.won = False
        self.lost = False
        self.scroll_limit = TILE_SIZE * 3
        self.scrolled = 0
        self.score = 0

        self.rect = pygame.Rect(x, y, CHARACTER_WIDTH, CHARACTER_HEIGHT)

    def update(self, level_map):
        self.level_map = level_map
        self.move(self.level_map)

        enemy_bullet_group = self.groups[2]
        if pygame.sprite.spritecollide(self, enemy_bullet_group, True):
            if self.health > 0:
                self.health -= 1
            else:
                self.alive = False
                self.lost = True
        self.draw()

    def move(self, level_map):
        delta_x = 0
        delta_y = 0
        obstacle_list = []
        lava_list = []
        self.level_map = level_map
        level_width = len(self.level_map[0]) * TILE_SIZE

        if self.move_left:
            delta_x -= SPEED
            self.direction = False
            
            #Scroll Left
            if self.rect.left + delta_x <= self.scroll_limit and self.scrolled != 0:
                self.scrolled -= SPEED
                delta_x = 0

        if self.move_right:
            delta_x += SPEED
            self.direction = True
            
            #Scroll Right
            if self.rect.right + delta_x >= SCREEN_WIDTH - self.scroll_limit:
                delta_x = 0
                if self.scrolled >= level_width - SCREEN_WIDTH:
                    self.scrolled = self.scrolled
                    delta_x += SPEED
                else:
                    self.scrolled += SPEED
                    
        # A jump (Make sure it jumps only once each time)
        if self.jumped and self.jumping == False:
            self.jumped = False
            self.jumping = True
            self.vertical_speed = -14

        self.vertical_speed += GRAVITY
        
        delta_y += self.vertical_speed

        for y, row in enumerate(range(12)):
          for x, tile in enumerate(range(48)):
                if self.level_map[y][x] == "1":
                    obstacle_tile = pygame.Rect(((x * TILE_SIZE) - self.scrolled, y * TILE_SIZE),(TILE_SIZE, TILE_SIZE))
                    obstacle_list.append(obstacle_tile)
                if self.level_map[y][x] == "2":
                    lava_tile = pygame.Rect(((x * TILE_SIZE) - self.scrolled, y * TILE_SIZE),(CHARACTER_WIDTH, CHARACTER_HEIGHT))
                    lava_list.append(lava_tile)

        for obstacle in obstacle_list:
            if obstacle.colliderect((self.rect.x + delta_x, self.rect.y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)):
                delta_x = 0
            if obstacle.colliderect((self.rect.x, self.rect.y + delta_y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)):
                if self.vertical_speed < 0:
                    self.vertical_speed = 0
                    delta_y = obstacle.bottom - self.rect.top
                elif self.vertical_speed >= 0:
                    self.jumping = False
                    self.vertical_speed = 0
                    delta_y = obstacle.top - self.rect.bottom

        if self.rect.left + delta_x < 0 or self.rect.right + delta_x > SCREEN_WIDTH:
                delta_x = 0
                  
        self.rect.x += delta_x
        self.rect.y += delta_y

    def draw(self):
        pygame.draw.rect(self.screen, "red", ((self.rect.x, self.rect.y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)))

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.y, self.direction)
        bullet_group = self.groups[3]
        bullet_group.add(bullet)
        self.ammonition -= 1