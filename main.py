import pygame
from variables import *
from maps import *

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
        self.jump = False
        self.move_right = False
        self.move_left = False
        self.shoot = False

    def update(self):
        self.move()
        self.draw()

    def move(self):
        delta_x = 0
        delta_y = 0

        if self.move_left:
            delta_x -= SPEED
        if self.move_right:
            delta_x += SPEED
        if self.jump:
            delta_y -= SPEED


        if platform_rect.colliderect((self.x + delta_x, self.y + delta_y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)):
            self.falling = False  
        else:
            self.falling = True
        
        if self.falling:
            delta_y += GRAVITY

        self.x += delta_x
        self.y += delta_y

    def draw(self):
        pygame.draw.rect(screen, "red", ((self.x, self.y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)))

t800 = Character(t800_x, t800_y)

while running:
        
    # Draw Background
    screen.fill("black")
    
    # Draw map
    platform_rect = pygame.draw.rect(screen, "blue", ((0, 540),(600, 30)))

    position_text = f"x: {t800.x} | y: {t800.y}"    
    text = font.render(position_text, True, "white")
    screen.blit(text, (10,40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # User input handling
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                t800.jump = True
            if event.key == pygame.K_RIGHT:
                t800.move_right = True
            if event.key == pygame.K_LEFT:
                t800.move_left = True

            if event.key == pygame.K_SPACE:
                shoot = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                t800.jump = False
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