import pygame
import sys
from variables import *
from character import *
from enemy import *
from menu import *
from bullet import *
from items import *
from map import *

class Game():
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Final - Juan Chaves")
        self.clock = pygame.time.Clock()
        self.initial_ticks = 0
        self.running = True
        self.font = pygame.font.SysFont("Futura", 30)
        self.playing = False 
        self.game_state = "main"
        self.new_game_started = False
        self.quitting_current_game = False
        self.game_ended = False
        self.current_level = 1
        self.lives = 3
        self.loading = 0
        self.level_map = []
        self.menu = Menu(self.screen)

        self.item_group = pygame.sprite.Group()
        self.transition_item_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.character_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.groups = []

        self.initial_game(self.current_level)
        self.state_handler()

    def initial_game(self, current_level):
        self.t800 = Character(t800_x, t800_y, self.screen, self.groups)

    def new_game(self, current_level):
        self.groups.append(self.item_group)
        self.groups.append(self.transition_item_group)
        self.groups.append(self.enemy_bullet_group)
        self.groups.append(self.bullet_group)

        self.current_level = current_level
        
        self.t800 = Character(t800_x, t800_y, self.screen, self.groups)
        self.map = Map(self.screen, self.t800, self.current_level, self.groups)
        self.character_group.add(self.t800)
        for coord in self.map.enemies_1():
            t1000 = Enemy(coord[1] * TILE_SIZE, coord[0] * TILE_SIZE, self.screen, self.t800, self.groups)
            self.enemy_group.add(t1000)
        self.level_map = self.map.process()
        self.initial_ticks = 0

    def reset_game(self, full_reset, level):
        if full_reset:
            self.current_level = level 
            self.lives = 3
            self.t800 = None
            self.map = None
            self.item_group.empty() 
            self.transition_item_group.empty()
            self.enemy_group.empty()
            self.character_group.empty()
            self.bullet_group.empty()
            self.enemy_bullet_group.empty()
            self.level_map.clear()
        else:
            self.current_level = level
            self.map = Map(self.screen, self.t800, self.current_level, self.groups)
            self.enemy_group.empty()
            self.level_map.clear()
            self.level_map = self.map.process()
        
    def state_handler(self):
        if self.menu.clicked:
            self.game_state = self.menu.get_clicked_btn()
            self.menu.clicked = False
        else:
            if self.game_state == "loading_next_level" and self.game_ended:
                self.game_state = "main"
                self.game_ended = False

        match self.game_state:
            case "main":
                self.current_level = 1
                if self.quitting_current_game == True:
                    self.initial_game(self.current_level)
                    self.quitting_current_game = False
                    self.game_ended = False
                self.lives = 3 
                self.restart_game()
                pygame.display.set_caption("Final - Juan Chaves")
                self.menu.show()

            case "play":
                playing_caption = f"Final - Juan Chaves | Level {self.current_level}"
                pygame.display.set_caption(playing_caption)
                self.game_ended = False
                
                if self.playing == False:
                    self.initial_ticks = pygame.time.get_ticks()
                self.playing = True
                self.show_game_info()
                self.show_clock(pygame.time.get_ticks() - self.initial_ticks)
                if self.t800.lost:
                    self.game_state = self.loose()
                if self.t800.won:
                    self.game_state = self.win()

            case "retry":
                self.menu.btn_id = "retry"
                self.menu.show()
                self.show_aftermath()
                if self.lives <= 0:
                    game_over_msg = "-GAME OVER-"
                    game_over_text = self.font.render(game_over_msg, True, "white")
                    self.screen.blit(game_over_text, (340, 300))

                if self.lives > 0: 
                    self.game_state = self.menu.get_clicked_btn()
                elif self.lives == 0 and self.menu.get_clicked_btn() == "main":
                    self.game_state = "main"
                    
                if self.game_state == "play":
                    self.restart_game()
                elif self.game_state == "main":
                    self.quitting_current_game = True

            case "loading_next_level":
                pygame.display.set_caption("Final - Juan Chaves")
                self.show_aftermath()
                self.loading += 1
                if self.loading == 40:
                    if not self.current_level <= 3:
                        self.reset_game(True, 1)
                        self.quitting_current_game = True
                        self.game_ended = True
                    else:
                        self.reset_game(False, self.current_level)
                        self.game_state = "play"
                        self.restart_game()
                    self.loading = 0
                
            case "settings":
                self.menu.show()
                pygame.display.set_caption("SETTINGS")

            case "levels":
                self.menu.show()
                pygame.display.set_caption("LEVELS")

            case "scores":
                self.menu.show()  
                pygame.display.set_caption("HIGH SCORES")

            case "about":
                self.menu.show()
                pygame.display.set_caption("ABOUT")

    def update(self):
        self.clock.tick(FPS)
        self.screen.fill("black")
        self.state_handler()
        if self.playing:
            if self.new_game_started == False:
                self.new_game(self.current_level)
                self.new_game_started = True
            self.map.update()
            self.map.draw()

            self.character_group.update(self.level_map)
            self.enemy_group.update(self.level_map)

            self.bullet_group.update()
            self.bullet_group.draw(self.screen)

            self.enemy_bullet_group.update()
            self.enemy_bullet_group.draw(self.screen)

            self.item_group.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # User input handling
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.t800.jumped = True
                    if event.key == pygame.K_RIGHT:
                        self.t800.move_right = True
                    if event.key == pygame.K_LEFT:
                        self.t800.move_left = True

                    if event.key == pygame.K_SPACE:
                        self.t800.shooting = True
                        if self.t800.ammonition > 0:
                            self.t800.shoot()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.t800.jumped = False
                    if event.key == pygame.K_RIGHT:
                        self.t800.move_right = False
                    if event.key == pygame.K_LEFT:
                        self.t800.move_left = False

                    if event.key == pygame.K_SPACE:
                        self.t800.shooting = False
        else:
            if self.game_state == "quit":
                pygame.quit()
                sys.exit()

        pygame.display.update()

    def show_clock(self, seconds):
        self.seconds = seconds // 1000
        total_time = 18 
        display_time = total_time - self.seconds
        last_ten = False
        if display_time > 69:
            time_msg = f"Time left: 01:{display_time - 60}"
        elif display_time > 59:
            time_msg = f"Time left: 01:0{display_time - 60}"
        elif display_time > 9:
            time_msg = f"Time left: 00:{display_time}"
        elif display_time >= 0:
            time_msg = f"Time left: 00:0{display_time}"
            last_ten = True
        else:
            time_msg = f"Time's Up"
            self.t800.lost = True

        if last_ten:
            time_text = self.font.render(time_msg, True, "Red")
        else:
            time_text = self.font.render(time_msg, True, "white")
        self.screen.blit(time_text, (600, 35))
    
    def show_game_info(self):
        health_msg = f"Health: {self.t800.health}"
        ammo_msg = f"Ammo: {self.t800.ammonition}"
        score_msg = f"Score: {self.t800.score}"

        health_text = self.font.render(health_msg, True, "white")
        ammo_text = self.font.render(ammo_msg, True, "white")
        score_text = self.font.render(score_msg, True, "white")

        self.screen.blit(health_text, (40, 35))
        self.screen.blit(ammo_text, (40, 65))
        self.screen.blit(score_text, (40, 95))

    def show_aftermath(self):
        score_msg = f"Your Score is: {self.t800.score}"
        lives_msg = f"Lives left: {self.lives}"
        if self.current_level >= 4:
            level_msg = "You completed all Levels!"
        else:
            level_msg = f"Current Level: {self.current_level}"
        score_text = self.font.render(score_msg, True, "white")
        lives_text = self.font.render(lives_msg, True, "white")
        level_text = self.font.render(level_msg, True, "white")
        self.screen.blit(score_text, (340, 350))
        self.screen.blit(lives_text, (340, 400))
        self.screen.blit(level_text, (340, 450))
    
    def loose(self):
        self.lives -= 1
        self.initial_ticks = 0
        self.playing = False

        return "retry"
    
    def win(self):
        if self.current_level <= 3:
            self.current_level += 1 
        else:
            self.current_level = 1
        self.playing = False
        
        return "loading_next_level"

    def restart_game(self):
        self.t800.rect.x = t800_x
        self.t800.rect.y = t800_y
        self.t800.position = (self.t800.x,self.t800.y)
        self.t800.vertical_speed = 0
        self.t800.jumped = False
        self.t800.jumping = False
        self.t800.move_right = False
        self.t800.move_left = False
        self.t800.direction = True
        self.t800.shooting = False
        self.t800.alive = True
        self.t800.ammonition = 10
        self.t800.health = 5
        self.t800.won = False
        self.t800.lost = False
        self.t800.scrolled = 0

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update()