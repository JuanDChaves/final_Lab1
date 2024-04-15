import pygame
from variables import *
from maps import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Final - Juan Chaves")
clock = pygame.time.Clock()
running = True

jump = False
move_right = False
move_left = False
shoot = False

font = pygame.font.SysFont("Futura", 30)

cur_t800_x = t800_x
cur_t800_y = t800_y

class Character():
    def __init__(self, x, y) -> None:
        self.position = (x,y)

    def draw(position):
        pygame.draw.rect(screen, "red", ((400, 400), (CHARACTER_WIDTH, CHARACTER_HEIGHT)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # User input handling
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                jump = True
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True

            if event.key == pygame.K_SPACE:
                shoot = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                jump = False
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False

            if event.key == pygame.K_SPACE:
                shoot = False
        
    # Draw Background
    # ###### THIS WILL BE REPLACED BY A BACKGROUND ########    
    screen.fill("black")
    
    # Draw map
    # ###### THIS WILL BE REPLACED BY A MAP ########
    platform_rect = pygame.draw.rect(screen, "blue", ((0, 540),(600, 30)))

    # Define hero's movement
    # Write a method that will return current (x,y)
    if move_left:
        cur_t800_x -= SPEED
    if move_right:
        cur_t800_x += SPEED
    if jump:
        cur_t800_y -= SPEED

    if falling:
        cur_t800_y += GRAVITY

    # Draw Hero
    hero_rect = pygame.draw.rect(screen, "blue", ((cur_t800_x, cur_t800_y), (CHARACTER_WIDTH, CHARACTER_HEIGHT)))

    t800 = Character(400,400)
    t800.draw()

    # Define collisions
    if hero_rect.colliderect((0, 540),(600, 30)):
        falling = False  
    else:
        falling = True

    position_text = f"x: {cur_t800_x} | y: {cur_t800_y}"    
    text = font.render(position_text, True, "white")
    screen.blit(text, (10,40))
    
    pygame.display.update()

    clock.tick(60)

pygame.quit()