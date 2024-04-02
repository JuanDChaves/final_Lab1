import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 700))
clock = pygame.time.Clock()
running = True

# To do
# Create a character Rectangle and flip
# Capture and store keyboard input
# Move the rectange
# Define gravity

jump = False
move_right = False
move_left = False
shoot = False

hero_height = 60
hero_width = 40
hero_inicial_x = 300
hero_inicial_y = 600


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
        

    screen.fill("black")

    if move_left:
        hero_inicial_x =- 0.25
    if move_right:
        hero_inicial_x =+ 0.25
    if jump:
        hero_inicial_y =+ 0.25

    pygame.draw.rect(screen, "white", ((hero_inicial_x, hero_inicial_y), (hero_width, hero_height)))

    pygame.display.update()

    clock.tick(60)

pygame.quit()