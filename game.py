import pygame
from pygame import mixer
import sys
from variables import *
from character import *
from enemy import *
from menu import * 
from bullet import *
from items import *
from map import *
import db

class Game():
    def __init__(self) -> None:
        mixer.init()
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.main_theme = pygame.mixer_music.load("./audio/main_theme.ogg")
        self.bg = pygame.image.load("./images/background/bg.jpg").convert()
        pygame.mixer_music.play(-1, 34)
        self.music_on = True
        self.sfx_on = True
        self.font = pygame.font.Font(None,32)
        pygame.display.set_caption("Final - Juan Chaves")
        self.clock = pygame.time.Clock()
        self.initial_ticks = 0
        self.running = True
        self.font = pygame.font.SysFont("Futura", 30)
        self.new_nick = ""
        self.current_nick = ""
        self.in_play = False 
        self.starting_game = False
        self.game_state = "main"
        self.game_over = False
        self.game_started = False
        self.to_next_level = False
        self.t800_curr_score = 0
        self.t800_curr_health = 0 
        self.playing_single_level = False
        self.single_level_started = False
        self.current_level = 1
        self.lives = 3 
        self.loading = 0
        self.level_map = []
        self.bg_image = None
        self.menu = Menu(self.screen)
        self.button_clicked_sound = pygame.mixer.Sound("./audio/button_clicked.ogg")
        db.create_db_table()

        self.item_group = pygame.sprite.Group()
        self.transition_item_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.character_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.groups = []

        self.state_handler()

    def new_game(self, current_level):
        self.groups.append(self.item_group)
        self.groups.append(self.transition_item_group)
        self.groups.append(self.enemy_bullet_group)
        self.groups.append(self.bullet_group)

        self.current_level = current_level
        
        self.t800 = Character(t800_x, t800_y, self.screen, self.groups)
        self.map = Map(self.screen, self.t800, self.current_level, self.groups)
        self.character_group.add(self.t800)
        if current_level == 1:
            for coord in self.map.enemies_1():
                t1000 = Enemy(coord[1] * TILE_SIZE, coord[0] * TILE_SIZE, self.screen, self.t800, self.groups)
                self.enemy_group.add(t1000)
        elif current_level == 2:
            for coord in self.map.enemies_2():
                t1000 = Enemy(coord[1] * TILE_SIZE, coord[0] * TILE_SIZE, self.screen, self.t800, self.groups)
                self.enemy_group.add(t1000)
        else:
            for coord in self.map.enemies_3():
                t1000 = Enemy(coord[1] * TILE_SIZE, coord[0] * TILE_SIZE, self.screen, self.t800, self.groups)
                self.enemy_group.add(t1000)
        
        if self.sfx_on == False:
            for enemy in self.enemy_group:
                enemy.sfx_on = False
        self.level_map = self.map.process()
        self.initial_ticks = pygame.time.get_ticks()

        self.load_bg(self.current_level)

        self.jump_sound = pygame.mixer.Sound("./audio/jump.ogg")
        self.shot_t800 = pygame.mixer.Sound("./audio/shot_t800.ogg")

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
            self.initial_ticks = pygame.time.get_ticks()
        else:
            self.t800.lost = False
            self.t800.won = False
            self.t800.rect.x = t800_x
            self.t800.scrolled = 0
            self.t800.alive = True
            self.current_level = level
            self.initial_ticks = pygame.time.get_ticks()
        
    def state_handler(self):
        if self.menu.clicked:
            if self.sfx_on:
                self.button_clicked_sound.play()
            self.game_state = self.menu.get_clicked_btn()
            if self.game_state == "playing_level_1" or self.game_state == "playing_level_2" or self.game_state == "playing_level_3":
                self.single_level_started = True
            self.menu.clicked = False
        
        match self.game_state:
            case "main":
                self.screen.blit(self.bg, (0,0))
                pygame.display.set_caption("Final - Juan Chaves")
                self.menu.show("main")
            
            case "nick_input":
                self.starting_game = True

            case "play":
                playing_caption = f"Final - Juan Chaves | Level {self.current_level}"
                pygame.display.set_caption(playing_caption)

                if self.in_play == False and self.game_started:
                    self.new_game(self.current_level)
                    if self.music_on:
                        self.play_guns_n_roses()
                    self.game_started = False
                elif self.in_play == False and self.game_started == False and self.to_next_level == False:
                    self.reset_game(False, self.current_level)
                if self.to_next_level:
                    self.new_game(self.current_level)     
                    self.t800.score = self.t800_curr_score
                    self.t800.health = self.t800_curr_health
                    self.to_next_level = False
            
                self.in_play = True
                
                if self.t800.lost:
                    self.game_state = self.loose()
                if self.t800.won:
                    self.game_state = self.win()

            case "play_level_1":
                self.current_level = 1
                self.play_single_level()
            
            case "play_level_2":
                self.current_level = 2
                self.play_single_level()

            case "play_level_3":
                self.current_level = 3
                self.play_single_level()

            case "retry":
                if self.lives <= 0:
                    self.game_state = "loading_next_level"
                    self.game_over = True
                else:
                    self.show_aftermath()
                    self.menu.show("retry")
                    self.game_state = self.menu.get_clicked_btn()
                    if self.game_state == "back":
                        self.reset_game(True, 1)
                        self.new_nick = ""
                        if self.music_on:
                            self.play_main_theme()

            case "loading_next_level":
                pygame.display.set_caption("Final - Juan Chaves")
                self.show_aftermath()
                self.loading += 1
                if self.loading == 240:
                    if self.playing_single_level == True:
                        self.reset_game(True, 1)
                        self.game_state = "main"
                        self.playing_single_level = False
                        if self.music_on:
                            self.play_main_theme()
                    else:
                        if self.game_over or self.current_level == 4:
                            db.insert_new_score(self.new_nick, self.t800.score)
                            self.reset_game(True, 1)
                            self.game_over = False
                            self.game_state = "main"
                            self.new_nick = ""
                            if self.music_on:
                                self.play_main_theme()
                        elif self.current_level < 4:
                            self.game_state = "play"
                            self.t800_curr_score = self.t800.score
                            self.t800_curr_health = self.t800.health
                            self.to_next_level = True
                            self.reset_game(True, self.current_level)
                    self.loading = 0
                
            case "audio":
                self.screen.blit(self.bg, (0,0))
                self.menu.show("audio")
                pygame.display.set_caption("AUDIO SETTINGS")
                music_msg = "MUSIC"
                sfx_msg = "SFX"
                music_text = self.font.render(music_msg, True, "white")
                sfx_text = self.font.render(sfx_msg, True, "white")
                self.screen.blit(music_text, (315, 215))
                self.screen.blit(sfx_text, (315, 315))
            
            case "onoff_music":
                self.screen.blit(self.bg, (0,0))
                if self.music_on:
                    pygame.mixer_music.stop()
                    self.music_on = False
                    self.game_state = "audio"
                elif self.music_on == False:
                    pygame.mixer_music.play(-1, 34)
                    self.music_on = True
                    self.game_state = "audio"
            
            case "onoff_sfx":
                self.screen.blit(self.bg, (0,0))
                if self.sfx_on == False:
                    self.sfx_on = True
                    self.game_state = "audio"
                elif self.sfx_on:
                    self.sfx_on = False
                    self.game_state = "audio"

            case "levels":
                self.screen.blit(self.bg, (0,0))
                self.menu.show("levels")
                pygame.display.set_caption("LEVELS")

            case "scores":
                self.screen.blit(self.bg, (0,0))
                self.menu.show("scores")  
                pygame.display.set_caption("HIGH SCORES")
                high_scores = db.show_high_scores()
                y = 200
                for score in high_scores:
                    score_msg = f"{score[0]}:{score[1]}"
                    score_text = self.font.render(score_msg, True, "white")
                    self.screen.blit(score_text, (300, y))
                    y += 40

            case "about":
                self.screen.blit(self.bg, (0,0))
                self.menu.show("about")
                pygame.display.set_caption("ABOUT")
                about_msg_1 = "FINAL PROGAMACION 1 - UTN"
                about_msg_2 = "Juan David Chaves"
                about_text_1 = self.font.render(about_msg_1, True, "white")
                about_text_2 = self.font.render(about_msg_2, True, "white")
                self.screen.blit(about_text_1, (250, 250))
                self.screen.blit(about_text_2, (300, 400))
            
            case "back":
                self.game_state = "main"

    def update(self):
        self.clock.tick(FPS)
        self.state_handler()

        if self.starting_game:
            self.screen.fill("black")
            input_msg = "What's your Nick?"
            restriction_msg = "No less than 3 characters"
            input_text = self.font.render(input_msg, True, "white")
            restriction_text = self.font.render(restriction_msg, True, "white")
            self.screen.blit(input_text, (300, 210))
            self.screen.blit(restriction_text, (250, 400))

            input_rect = pygame.Rect(310,250,140,32)
            pygame.draw.rect(self.screen, 'lightskyblue3', input_rect, 2)
            text_surface = self.font.render(self.new_nick, True, (255,255,255))
            self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y +5))
            go_btn = pygame.image.load(f"./images/buttons/go_btn.png").convert_alpha()
            go_btn = pygame.transform.scale_by(go_btn, 0.5)
            self.screen.blit(go_btn, (300, 300))
            go_rect = pygame.Rect((300 + 10,300 + 10),(go_btn.get_width() - 20, go_btn.get_height() - 20))
            self.pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and len(self.new_nick) >= 3:
                    if pygame.Rect.collidepoint(go_rect, self.pos):
                        if self.sfx_on:
                            self.button_clicked_sound.play()
                        self.game_state = "play"
                        self.game_started = True
                        self.starting_game = False
                if event.type == pygame.TEXTINPUT:
                    if len(self.new_nick) > 10:
                        self.new_nick = self.new_nick
                    else:
                        self.new_nick += event.text
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.new_nick = self.new_nick[0:-1]
            

        if self.in_play:
            self.screen.fill("black")
            self.draw_bg()
            self.show_game_info()
            self.show_clock(pygame.time.get_ticks() - self.initial_ticks)

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
                        if self.sfx_on:
                            self.jump_sound.play()
                    if event.key == pygame.K_RIGHT:
                        self.t800.move_right = True
                    if event.key == pygame.K_LEFT:
                        self.t800.move_left = True

                    if event.key == pygame.K_SPACE:
                        self.t800.shooting = True
                        if self.t800.ammonition > 0:
                            self.t800.shoot()
                            if self.sfx_on:
                                self.shot_t800.play()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.t800.jumped = False
                    if event.key == pygame.K_RIGHT:
                        self.t800.move_right = False
                    if event.key == pygame.K_LEFT:
                        self.t800.move_left = False

                    if event.key == pygame.K_SPACE:
                        self.t800.shooting = False
        if self.game_state == "quit":
            db.delete_db_table()
            pygame.quit()
            sys.exit()

        pygame.display.update()

    def play_single_level(self):
        self.playing_single_level = True
        self.single_level_started = True
        playing_caption = f"Final - Juan Chaves | Level {self.current_level}"
        pygame.display.set_caption(playing_caption)
        if self.in_play == False and self.single_level_started:
            self.new_game(self.current_level)
            self.single_level_started = False
            if self.music_on:
                self.play_guns_n_roses()
        self.in_play = True
        self.show_game_info()
        self.show_clock(pygame.time.get_ticks() - self.initial_ticks)

        if self.t800.lost or self.t800.won:
            self.in_play = False
            self.game_state = "loading_next_level"
    
    def play_main_theme(self):
        pygame.mixer_music.stop()
        pygame.mixer_music.unload()
        pygame.mixer_music.load("./audio/main_theme.ogg")
        pygame.mixer_music.play(-1, 34)

    
    def play_guns_n_roses(self):
        pygame.mixer_music.stop()
        pygame.mixer_music.unload()
        pygame.mixer_music.load("./audio/you_could_be_mine.ogg")
        pygame.mixer_music.play(-1, 46, 2000)

    def show_clock(self, seconds):
        self.seconds = seconds // 1000
        total_time = 25 
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
        self.screen.fill("black")
        if self.game_over:
            game_over_msg = "-GAME OVER-"
            game_over_text = self.font.render(game_over_msg, True, "white")
            self.screen.blit(game_over_text, (340, 200))
        elif self.playing_single_level:
            score_msg = f"Your Score is: {self.t800.score}"
            level_msg = f"You Played Level: {self.current_level}"
            score_text = self.font.render(score_msg, True, "white")
            level_text = self.font.render(level_msg, True, "white")
            self.screen.blit(score_text, (340, 250))
            self.screen.blit(level_text, (340, 350))
        else:
            nick_msg = f"--- {self.new_nick} ---"
            score_msg = f"Your Score is: {self.t800.score}"
            lives_msg = f"Lives left: {self.lives}"
            if self.current_level >= 4:
                level_msg = "You completed all Levels!"
            else:
                level_msg = f"Current Level: {self.current_level}"
            nick_text = self.font.render(nick_msg, True, "white")
            score_text = self.font.render(score_msg, True, "white")
            lives_text = self.font.render(lives_msg, True, "white")
            level_text = self.font.render(level_msg, True, "white")
            self.screen.blit(nick_text, (340, 200))
            self.screen.blit(score_text, (340, 250))
            self.screen.blit(lives_text, (340, 300))
            self.screen.blit(level_text, (340, 350))
    
    def loose(self):
        self.lives -= 1
        self.in_play = False
        return "retry"
    
    def win(self):
        if self.current_level <= 3:
            self.current_level += 1 
        else:
            self.current_level = 1
        self.in_play = False
        
        return "loading_next_level"
    
    def load_bg(self, level):
        self.bg_image = pygame.image.load(f"./images/background/{level}.png")
        self.bg_image = pygame.transform.scale_by(self.bg_image, 0.4)

    def draw_bg(self):
        for x in range(5):

            self.screen.blit(self.bg_image, (x * SCREEN_WIDTH - self.t800.scrolled, 0))
    
    # -- VERSION PARALAX --
    # def load_bg(self, level):
    #     for i in range(1, 6):
    #         bg_image = pygame.image.load(f"./images/paralax_bg/city_{level}/{i}.png")
    #         bg_image = pygame.transform.scale_by(bg_image, 1.7)
    #         self.bg_images.append(bg_image)
            
    # def draw_bg(self):
    #     for x in range(5):
    #         speed = 1
    #         for image in self.bg_images:
    #             self.screen.blit(image, ((x * SCREEN_WIDTH) - self.t800.scrolled * speed, 0))
    #             speed += 0.04

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    db.delete_db_table()
                    pygame.quit()
                    sys.exit()

            self.update()