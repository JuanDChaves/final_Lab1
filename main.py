import pygame
from variables import *
from maps import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

jump = False
move_right = False
move_left = False
shoot = False

cur_hero_x = hero_x
cur_hero_y = hero_y

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
    screen.fill("black")

    # Draw map
    platform_rect = pygame.draw.rect(screen, "white", ((600, 300),(200, 30)))

    # Define hero's movement
    # Write a method that will return current (x,y)
    if move_left:
        cur_hero_x -= SPEED
    if move_right:
        cur_hero_x += SPEED
    if jump:
        cur_hero_y -= SPEED * 2

    if falling:
        cur_hero_y += GRAVITY

    # Draw Hero
    hero_rect = pygame.draw.rect(screen, "white", ((cur_hero_x, cur_hero_y), (HERO_WIDTH, HERO_HEIGHT)))

    # Define collisions
    if hero_rect.colliderect((600, 300),(200, 30)):
        falling = False  
    else:
        falling = True
    pygame.display.update()

    clock.tick(60)

pygame.quit()