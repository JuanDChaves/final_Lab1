import pygame
from variables import *
# from maps import *
# from mapstest import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Final - Juan Chaves")
clock = pygame.time.Clock()
running = True

font = pygame.font.SysFont("Futura", 30)

class Character():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.position = (x,y)
        self.falling = True
        self.vertical_speed = 0
        self.jumped = False
        self.jumping = False
        self.move_right = False
        self.move_left = False
        self.shoot = False

    def update(self):
        self.move()
        self.draw()

    def move(self):
        delta_x = 0
        delta_y = 0

        # for y, row in enumerate(range(12)):
        #   for x, tile in enumerate(range(18)):
        #         if level_map[y, x] == "1":
                
        #         else:


        if self.move_left:
            delta_x -= SPEED
            if self.falling and platform_rect.colliderect((self.x + delta_x, self.y + delta_y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)):
                delta_x += SPEED
        if self.move_right:
            delta_x += SPEED
            if self.falling and platform_rect.colliderect((self.x + delta_x, self.y + delta_y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)):
                delta_x -= SPEED
        
        if self.jumped and self.jumping == False:
            self.jumped = False
            self.jumping = True
            self.vertical_speed = -15

        if self.jumped == False and self.jumping or self.falling:
            self.vertical_speed += GRAVITY
        
        delta_y += self.vertical_speed
        
        if platform_rect.colliderect((self.x + delta_x, self.y + delta_y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)):
            self.falling = False
            self.jumping = False
            self.vertical_speed = 0
        else:
            self.falling = True

        # if self.move_left:
        #     delta_x -= SPEED
        #     if self.falling and platform_rect.colliderect((self.x + delta_x, self.y + delta_y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)):
        #         delta_x += SPEED
        # if self.move_right:
        #     delta_x += SPEED
        #     if self.falling and platform_rect.colliderect((self.x + delta_x, self.y + delta_y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)):
        #         delta_x -= SPEED
        
        # if self.jumped and self.jumping == False:
        #     self.jumped = False
        #     self.jumping = True
        #     self.vertical_speed = -15

        # if self.jumped == False and self.jumping or self.falling:
        #     self.vertical_speed += GRAVITY
        
        # delta_y += self.vertical_speed
        
        # if platform_rect.colliderect((self.x + delta_x, self.y + delta_y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)):
        #     self.falling = False
        #     self.jumping = False
        #     self.vertical_speed = 0
        # else:
        #     self.falling = True

        self.x += delta_x
        self.y += delta_y

    def draw(self):
        pygame.draw.rect(screen, "red", ((self.x, self.y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)))

#######################
# MAP
#######################

class Map:
    def __init__(self) -> None:
        self.level = []

    def update(self):
        pass

    def draw(self):
        pass

    def map_1(self):
        level = [
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "1", "1", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "1", "1", "0"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "0", "0", "0", "0", "0", "1", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "0", "0", "1", "1", "1", "1", "1", "1"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ]
        return level

t800 = Character(t800_x, t800_y)
map = Map()

#######################
# LOOP
#######################

while running:
        
    # Draw Background
    screen.fill("black")
    
    # Draw map
    level_map = map.map_1()
    tile = None
    for y, row in enumerate(range(12)):
        for x, tile in enumerate(range(18)):
            if level_map[y][x] == "1":
                tile = pygame.draw.rect(screen, "Gray", ((x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
            else:
                tile = pygame.draw.rect(screen, "Gray", ((x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)),1)
    
    platform_rect = pygame.draw.rect(screen, "blue", ((0, 540),(600, 30)))

    position_text = f"x: {t800.x} | y: {t800.y} | v_speed: {t800.vertical_speed}"    
    text = font.render(position_text, True, "white")
    screen.blit(text, (10,40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # User input handling
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                t800.jumped = True
            if event.key == pygame.K_RIGHT:
                t800.move_right = True
            if event.key == pygame.K_LEFT:
                t800.move_left = True

            if event.key == pygame.K_SPACE:
                shoot = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                t800.jumped = False
            if event.key == pygame.K_RIGHT:
                t800.move_right = False
            if event.key == pygame.K_LEFT:
                t800.move_left = False

            if event.key == pygame.K_SPACE:
                shoot = False
    
    t800.update()
    pygame.display.update()

    clock.tick(60)

pygame.quit()