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
        self.alive = True
        self.groups = groups
        self.current_frame = 0
        self.animation_cooldown = 0
        self.current_sheet_type = "running"
        self.direction = True # True = Right, False = Left
        self.patrol_area = 0
        self.visual_field = 200
        self.idle = True
        self.cooldown = 40
        self.health = 3
        self.recharging = False
        self.shot_t1000 = pygame.mixer.Sound("./audio/shot_t1000.ogg")
        self.sfx_on = True

        self.rect = pygame.Rect(x, y, CHARACTER_WIDTH, CHARACTER_HEIGHT)

    def update(self, level):
        self.level_map = level
        if self.alive:
            self.move()
        sheet = ""

        bullet_count = 0
        current_rect = pygame.Rect(self.rect.x - self.t800.scrolled ,self.rect.y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        bullet_group = self.groups[3]

        for bullet in bullet_group:
            bullet_count += 1
            if pygame.Rect.colliderect(current_rect, bullet.rect):
                bullet.kill()
                self.health -= 1
                self.t800.score += 5
        
        if self.health == 0 and self.alive:
            self.t800.score += 10
            self.alive = False
        
        if self.idle and self.alive:
            sheet = "running"
        elif not self.idle and self.alive:
            sheet = "idle"
        elif not self.alive:
            sheet = "killed"
        self.draw(sheet)

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
                    if self.sfx_on:
                        self.shot_t1000.play()
                    self.shoot(current_x)
                    self.recharging = True
            else:
                self.idle = True
        elif self.direction == False:
            if self.t800.rect.colliderect(self.rect.x - self.t800.scrolled - self.visual_field, self.rect.y, CHARACTER_WIDTH + self.visual_field, CHARACTER_HEIGHT) and self.t800.alive == True:
                self.idle = False
                if self.cooldown == 40:
                    current_x = self.rect.x - self.t800.scrolled
                    if self.sfx_on:
                        self.shot_t1000.play()
                    self.shoot(current_x)
                    self.recharging = True
            else:
                self.idle = True

    def get_image(self, sheet, frame):
        self.sheet = sheet
        self.frame = frame
        image = pygame.Surface((48, 48)).convert_alpha()
        image.blit(self.sheet, (0, 0), (self.frame * 48, 0, 48, 48))
        image = pygame.transform.scale_by(image, 1.5)
        if not self.direction:
            image = pygame.transform.flip(image, True, False)
        image.set_colorkey("black")

        return image

    def draw(self, type):
        if not type == "":
            self.sheet_type = type
        if not self.sheet_type == self.current_sheet_type:
            self.current_sheet_type = self.sheet_type
            self.current_frame = 0
        current_sheet = pygame.image.load(f"./images/sprites/t1000_{self.sheet_type}.png").convert_alpha()
        frames_list = []
        total_frames = int(current_sheet.get_width() / 48)
        for i in range(int(total_frames)):
            image = self.get_image(current_sheet, i)
            frames_list.append(image)
        
        self.animation_cooldown += 1

        if self.animation_cooldown == 10:
            self.current_frame += 1
            if self.current_frame > len(frames_list) - 1:
                if self.sheet_type == "killed":
                    self.current_frame = 7
                else:
                    self.current_frame = 0
            self.animation_cooldown = 0
        
        self.screen.blit(frames_list[self.current_frame], (self.rect.x - self.t800.scrolled - 20, self.rect.y))
        frames_list.clear()

    def shoot(self, current_x):
        bullet = Bullet(current_x, self.rect.y, self.direction)
        enemy_bullet_group = self.groups[2]
        enemy_bullet_group.add(bullet)