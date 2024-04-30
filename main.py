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
        self.scrolled = 0
        self.scroll = False

        self.rect = pygame.Rect(x, y, CHARACTER_WIDTH, CHARACTER_HEIGHT)

    def update(self):
        self.move()
        self.draw()

    def move(self):
        delta_x = 0
        delta_y = 0
        obstacle_list = []

        if self.move_left:
            delta_x -= SPEED

            if self.rect.x + delta_x + self.scrolled <= TILE_SIZE * 3:
                self.scrolled = 0
                self.scroll = False
                if self.rect.x + delta_x <= 0:
                    delta_x = 0

        if self.move_right:
            delta_x += SPEED
            if (self.rect.x + CHARACTER_WIDTH) + delta_x >= SCREEN_WIDTH:
                delta_x = 0
            
            #Scroll
            if (self.rect.x + CHARACTER_WIDTH) + delta_x >= SCREEN_WIDTH - (TILE_SIZE * 3):
                self.scrolled += SPEED
                self.scroll = True
        
        # A jump (Make sure it jumps only once each time)
        if self.jumped and self.jumping == False:
            self.jumped = False
            self.jumping = True
            self.vertical_speed = -14

        self.vertical_speed += GRAVITY
        
        delta_y += self.vertical_speed

        for y, row in enumerate(range(12)):
          for x, tile in enumerate(range(18)):
                if level_map[y][x] == "1":
                    obstacle_tile = pygame.Rect(((x * TILE_SIZE) - self.scrolled, y * TILE_SIZE),(CHARACTER_WIDTH, CHARACTER_HEIGHT))
                    obstacle_list.append(obstacle_tile)

        for obstacle in obstacle_list:
            if obstacle.colliderect((self.rect.x + delta_x, self.rect.y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)):
                delta_x = 0
            if obstacle.colliderect((self.rect.x, self.rect.y + delta_y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)):
                if self.vertical_speed < 0:
                    self.vertical_speed = 0
                    delta_y = obstacle.bottom - self.rect.top
                elif self.vertical_speed >= 0:
                    self.falling = False
                    self.jumping = False
                    self.vertical_speed = 0
                    delta_y = obstacle.top - self.rect.bottom

            if self.rect.left + delta_x < 0 or self.rect.right + delta_x > SCREEN_WIDTH:
                    delta_x = 0
                  
        self.rect.x += delta_x
        self.rect.y += delta_y


    def draw(self):
        pygame.draw.rect(screen, "red", ((self.rect.x, self.rect.y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)))

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
                    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "0", "1", "1", "1", "1", "1", "1", "1"],
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
        
    clock.tick(FPS)
    # Draw Background
    screen.fill("black")
    
    # Draw map
    level_map = map.map_1()
    t800.update()
    tile = None
    for y, row in enumerate(range(12)):
        for x, tile in enumerate(range(18)):
            if level_map[y][x] == "1":
                tile = pygame.draw.rect(screen, "Gray", (((x * TILE_SIZE) - t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
            else:
                tile = pygame.draw.rect(screen, "Gray", (((x * TILE_SIZE) - t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)),1)

    position_text = f"x: {t800.rect.x} | y: {t800.rect.y} | v_speed: {t800.vertical_speed}"    
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
    
    pygame.display.update()


pygame.quit()