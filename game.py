import pygame as pg

import sprites
from menu import MainMenu
from objects import Button, Picture
from sprites import Player, Enemy

from objects import Button, Picture


pg.init()


class Game:
    def __init__(self):
        pg.init()
        self.running, self.playing = True, False
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 720
        self.window = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen = pg.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.FPS = 60
        self.font_name = "fonts/pixfont.ttf"
        self.frame_per_second = pg.time.Clock()

        self.clicked = False

        self.speed = 8

        # MENU
        self.main_menu = MainMenu(self)
        button_sound = pg.mixer.Sound("audio/button_sound.mp3")

        title_image = pg.image.load("images/title_name.png")
        self.title_picture = Picture((self.SCREEN_WIDTH - title_image.get_width()) // 2, 20, title_image, 1)

        start_but_off = pg.image.load("images/buttons/start_button_off.png").convert_alpha()
        start_but_on = pg.image.load("images/buttons/start_button_on.png").convert_alpha()
        self.start_button = Button(370, 247, start_but_off, start_but_on, button_sound, 0.3)

        garage_but_off = pg.image.load("images/buttons/garage_button_off.png").convert_alpha()
        garage_but_on = pg.image.load("images/buttons/garage_button_on.png").convert_alpha()
        self.garage_button = Button(655, 247, garage_but_off, garage_but_on, button_sound, 0.3)

        music_but_off = pg.image.load("images/buttons/music_button_off.png").convert_alpha()
        music_but_on = pg.image.load("images/buttons/music_button_on.png").convert_alpha()
        self.music_button = Button(370, 367, music_but_off, music_but_on, button_sound, 0.3)

        sets_but_off = pg.image.load("images/buttons/settings_button_off.png").convert_alpha()
        sets_but_on = pg.image.load("images/buttons/settings_button_on.png").convert_alpha()
        self.sets_button = Button(655, 367, sets_but_off, sets_but_on, button_sound, 0.3)

        quit_but_off = pg.image.load("images/buttons/quit_button_off.png").convert_alpha()
        quit_but_on = pg.image.load("images/buttons/quit_button_on.png").convert_alpha()
        self.quit_button = Button(512, 487, quit_but_off, quit_but_on, button_sound, 0.3)

        close_but_off = pg.image.load("images/buttons/close_button_off.png").convert_alpha()
        close_but_on = pg.image.load("images/buttons/close_button_on.png").convert_alpha()
        self.close_button = Button(530, 300, close_but_off, close_but_on, button_sound, 0.25)

        back_but_off = pg.image.load("images/buttons/back_button_off.png").convert_alpha()
        back_but_on = pg.image.load("images/buttons/back_button_on.png").convert_alpha()
        self.back_button = Button(645, 300, back_but_off, back_but_on, button_sound, 0.25)

        # BACKGROUND
        bg_summer_img = pg.image.load("images/backgrounds/background.png")
        self.bg_summer = Picture(0, 0, bg_summer_img)
        self.bg_summer.resize(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.game_state = "GAME"

        # IMAGES FOR GAME
        '''player_car_1 = pg.image.load("images/cars/player_car_1.gif")
        self.player_car_1 = Picture(750, 450, player_car_1, 1.1)'''
        '''self.player_car_1 = self.player_car_1.extractFrames("images/cars/player_car_1.gif")'''

        '''enemy_car_1 = pg.image.load("images/cars/opp1.png")
        self.enemy_car_1 = Picture(450, 100, enemy_car_1, 1.1)'''
        crash = pg.image.load('images/crash.png')

        player_group = pg.sprite.Group()
        vehicle_group = pg.sprite.Group()



        self.P1 = Player("images/cars/player_car_1.png", 750, 500)
        self.P1.set_speed(self.speed)
        player = sprites.Car("images/cars/player_car_1.png", 750, 500)
        player_group.add(player)

        self.E1 = Enemy("images/cars/opp1.png")
        self.P1.set_speed(self.speed)
        self.E1.set_speed(self.speed)


    def game_loop(self):
        #enemies_list = pg.sprite.Group()
        #all_sprites_list = pg.sprite.Group()

        #enemies_list.add(E1)
        #all_sprites_list.add(P1)

        while self.playing:
            self.check_events()
            self.P1.set_speed(self.speed)
            self.E1.set_speed(self.speed)

            self.screen.blit(self.bg_summer.image, self.bg_summer.rect)
            self.screen.blit(self.bg_summer.image, (self.bg_summer.rect[0], self.bg_summer.rect[1] - self.SCREEN_HEIGHT))

            if self.game_state == "GAME":
                if self.bg_summer.rect[1] == self.SCREEN_HEIGHT:
                    self.bg_summer.rect.topleft = (0, 0)
                self.bg_summer.rect[1] += self.speed

            self.P1.move(self.screen)
            self.E1.move(self.screen)

            if self.game_state == "PAUSED":
                self.speed = 0
                if self.close_button.draw(self.screen):
                    self.playing = False
                    self.speed = 8

                if self.back_button.draw(self.screen):
                    self.game_state = "GAME"
                    self.speed = 8

            self.window.blit(self.screen, (0, 0))
            pg.display.update()
            self.frame_per_second.tick(self.FPS)
            self.reset_keys()
            if not self.playing:
                pg.time.delay(500)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT and self.running and self.playing:
                self.running, self.playing = False, False
                self.main_menu.run_display = True
            if event.type == pg.KEYDOWN:
                '''if event.key in [pg.K_a, pg.K_LEFT] and self.player_car_1.rect[0] != 450:
                    self.player_car_1.rect = self.player_car_1.rect.move([-300, 0])
                if event.key in [pg.K_d, pg.K_RIGHT] and self.player_car_1.rect[0] != 750:
                    self.player_car_1.rect = self.player_car_1.rect.move([300, 0])'''
                if event.key == pg.K_ESCAPE:
                    if self.game_state == "PAUSED":
                        self.game_state = "GAME"
                        self.speed = 8
                    else:
                        self.game_state = "PAUSED"
                    print(self.game_state)

    def reset_keys(self):
        self.screen = pg.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def draw_text(self, text, size, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    class Moving:
        def __init__(self):
            self.i = 0
