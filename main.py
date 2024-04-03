import pygame
from variables import *

pygame.init()
screen = pygame.display.set_mode((1280, 700))
clock = pygame.time.Clock()
running = True

jump = False
move_right = False
move_left = False
shoot = False

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
    platform_rect = pygame.draw.rect(screen, "white", ((900, 400),(200, 30)))


    # Define hero's movement
    if move_left:
        hero_x -= SPEED
    if move_right:
        hero_x += SPEED
    if jump:
        hero_y -= SPEED * 2

    hero_y += GRAVITY

    # Draw Hero
    hero_rect = pygame.draw.rect(screen, "white", ((hero_x, hero_y), (HERO_WIDTH, HERO_HEIGHT)))

    # Define co
    if hero_rect.colliderect(platform_rect):

        print(f"collision {hero_rect.x, hero_rect.y}")

    pygame.display.update()

    clock.tick(60)

pygame.quit()