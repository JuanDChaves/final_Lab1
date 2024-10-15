import pygame
from variables import *
from bullet import *

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, groups):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.current_sheet_type = "idle"
        self.sheet_type = None
        self.animation_cooldown = 0 
        self.current_frame = 0
        self.screen = screen
        self.groups = groups
        self.position = (x,y)
        self.vertical_speed = 0
        self.idle = True
        self.jumped = False
        self.jumping = False
        self.landed = True
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
        sheet = "" 


        enemy_bullet_group = self.groups[2]
        if pygame.sprite.spritecollide(self, enemy_bullet_group, True):
            if self.health > 0:
                self.health -= 1
            else:
                self.alive = False
                self.lost = True

        if self.idle and self.landed:
            sheet = "idle"
        if self.move_right and self.landed:
            sheet = "running"
        if self.move_left and self.landed:
            sheet = "running"
        if self.jumping and not self.landed:
            sheet = "jump"

        self.draw(sheet)

    def move(self, level_map):
        delta_x = 0
        delta_y = 0
        obstacle_list = []
        lava_list = []
        self.level_map = level_map
        level_width = len(self.level_map[0]) * TILE_SIZE

        if self.move_left: 
            self.idle = False
            delta_x -= SPEED
            self.direction = False
        
            if self.rect.left + delta_x <= self.scroll_limit and self.scrolled != 0:
                self.scrolled -= SPEED
                delta_x = 0
        else:
            self.idle = True

        if self.move_right:
            self.idle = False
            delta_x += SPEED
            self.direction = True
        
            if self.rect.right + delta_x >= SCREEN_WIDTH - self.scroll_limit:
                delta_x = 0
                if self.scrolled >= level_width - SCREEN_WIDTH:
                    self.scrolled = self.scrolled
                    delta_x += SPEED
                else:
                    self.scrolled += SPEED
        if self.jumped and self.jumping == False:
            self.landed = False
            self.jumped = False
            self.jumping = True
            self.vertical_speed = -14

        self.vertical_speed += GRAVITY
        
        delta_y += self.vertical_speed

        for y, row in enumerate(range(12)):
          for x, tile in enumerate(range(48)):
                if int(self.level_map[y][x]) >= 1 and int(self.level_map[y][x]) <= 81:
                    obstacle_tile = pygame.Rect(((x * TILE_SIZE) - self.scrolled, y * TILE_SIZE),(TILE_SIZE, TILE_SIZE))
                    obstacle_list.append(obstacle_tile)
                if self.level_map[y][x] == "88":
                    lava_tile = pygame.Rect(((x * TILE_SIZE) - self.scrolled, y * TILE_SIZE),(CHARACTER_WIDTH, CHARACTER_HEIGHT))
                    lava_list.append(lava_tile)

        for obstacle in obstacle_list:
            if obstacle.colliderect((self.rect.x + delta_x, self.rect.y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)):
                delta_x = 0
                self.landed = True
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
        current_sheet = pygame.image.load(f"./images/sprites/t800_{self.sheet_type}.png").convert_alpha()
        frames_list = []
        total_frames = int(current_sheet.get_width() / 48)
        for i in range(int(total_frames)):
            image = self.get_image(current_sheet, i)
            frames_list.append(image)
        
        self.animation_cooldown += 1

        if self.animation_cooldown == 10:
            self.current_frame += 1
            if self.current_frame > len(frames_list) - 1:
                self.current_frame = 0
            self.animation_cooldown = 0

        self.screen.blit(frames_list[self.current_frame], (self.rect.x - 20, self.rect.y + 5))
        frames_list.clear()

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.y, self.direction)
        bullet_group = self.groups[3]
        bullet_group.add(bullet)
        self.ammonition -= 1