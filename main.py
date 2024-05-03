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
        self.vertical_speed = 0
        self.jumped = False
        self.jumping = False
        self.move_right = False
        self.move_left = False
        self.shoot = False
        self.scroll_limit = TILE_SIZE * 3
        self.scrolled = 0

        self.rect = pygame.Rect(x, y, CHARACTER_WIDTH, CHARACTER_HEIGHT)

    def update(self):
        self.move()
        self.draw()

    def move(self):
        delta_x = 0
        delta_y = 0
        obstacle_list = []
        level_width = len(level_map[0]) * TILE_SIZE

        if self.move_left:
            delta_x -= SPEED
            
            #Scroll Left
            if self.rect.left + delta_x <= self.scroll_limit and self.scrolled != 0:
                self.scrolled -= SPEED
                delta_x = 0

        if self.move_right:
            delta_x += SPEED
            
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
                    self.jumping = False
                    self.vertical_speed = 0
                    delta_y = obstacle.top - self.rect.bottom

        if self.rect.left + delta_x < 0 or self.rect.right + delta_x > SCREEN_WIDTH:
                delta_x = 0
                  
        self.rect.x += delta_x
        self.rect.y += delta_y


    def draw(self):
        pygame.draw.rect(screen, "red", ((self.rect.x, self.rect.y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)))

    def shoot(self):
        pass

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
        # 24 x 12
        level = [
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "5", "5", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "5", "5"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "5", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "5", "5", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "3", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "1", "1", "0", "0", "0", "1", "1", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "4", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "5", "5", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "1", "1", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "1", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "0", "0", "0", "0", "0", "1", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "8", "0"],
                    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "0", "0", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "0", "0", "0", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
                    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
                    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]
                ]
        return level

t800 = Character(t800_x, t800_y)
t1000 = Character(t800_x + 300, t800_y)
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
    # t1000.update()
    tile = None
    for y, row in enumerate(range(12)):
        for x, tile in enumerate(range(48)):
            # 1 Block = saddlebrown
            # 2 lava = organgered
            # 3 Health = crimson
            # 4 Ammo = orange
            # 5 Deco1 = paleturquoise
            # 6 Deco2 = papayawhip
            # 7 Deco3 = palegreen
            # 8 Exit = gold
            # T800 = blue
            # T1000 = black
            if level_map[y][x] == "1":
                tile = pygame.draw.rect(screen, "saddlebrown", (((x * TILE_SIZE) - t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
            elif level_map[y][x] == "2":
                tile = pygame.draw.rect(screen, "orangered", (((x * TILE_SIZE) - t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
            elif level_map[y][x] == "3":
                tile = pygame.draw.rect(screen, "crimson", (((x * TILE_SIZE) - t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
            elif level_map[y][x] == "4":
                tile = pygame.draw.rect(screen, "orange", (((x * TILE_SIZE) - t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
            elif level_map[y][x] == "5":
                tile = pygame.draw.rect(screen, "paleturquoise", (((x * TILE_SIZE) - t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
            elif level_map[y][x] == "6":
                tile = pygame.draw.rect(screen, "papayawhip", (((x * TILE_SIZE) - t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
            elif level_map[y][x] == "7":
                tile = pygame.draw.rect(screen, "palegreen", (((x * TILE_SIZE) - t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
            elif level_map[y][x] == "8":
                tile = pygame.draw.rect(screen, "gold", (((x * TILE_SIZE) - t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
                
            # else:
            #     tile = pygame.draw.rect(screen, "Gray", (((x * TILE_SIZE) - t800.scrolled, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)),1)

    position_text = f"x: {t800.rect.x} | y: {t800.rect.y} | scrolled: {t800.scrolled}"    
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