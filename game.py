import pygame as pg
from menu import MainMenu
from objects import Button, Picture, Background
from sprites import Player, Enemy

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

        # MENU
        self.main_menu = MainMenu(self)
        button_sound = pg.mixer.Sound("audio/button_sound.mp3")

        self.title_picture = Picture(130, 20, "images/title_name.png", 1)
        self.start_button = Button(370, 247, "images/buttons/start_button_off.png", "images/buttons/start_button_on.png", button_sound, 0.3)
        self.garage_button = Button(655, 247, "images/buttons/garage_button_off.png", "images/buttons/garage_button_on.png", button_sound, 0.3)
        self.music_button = Button(370, 367, "images/buttons/music_button_off.png", "images/buttons/music_button_on.png", button_sound, 0.3)
        self.sets_button = Button(655, 367, "images/buttons/settings_button_off.png", "images/buttons/settings_button_on.png", button_sound, 0.3)
        self.quit_button = Button(512, 487, "images/buttons/quit_button_off.png", "images/buttons/quit_button_on.png", button_sound, 0.3)
        self.close_button = Button(530, 300, "images/buttons/close_button_off.png", "images/buttons/close_button_on.png", button_sound, 0.25)
        self.back_button = Button(645, 300, "images/buttons/back_button_off.png", "images/buttons/back_button_on.png", button_sound, 0.25)

        # BACKGROUND
        self.bg_summer = Background("images/backgrounds/background.png")
        self.bg_summer.resize(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # CARS
        self.player_car_1 = Picture(750, 450, "images/cars/player_car_1.png", 1.1)
        self.enemy_car_1 = Picture(450, 100, "images/cars/opp1.png", 1.1)

        self.speed = 10

        self.game_state = "GAME"

    def game_loop(self):

        #enemies_list = pg.sprite.Group()
        #all_sprites_list = pg.sprite.Group()

        P1 = Player("images/cars/player_car_1.png", 750, 450)
        E1 = Enemy("images/cars/opp1.png")

        #enemies_list.add(E1)
        #all_sprites_list.add(P1)

        P1.set_speed(self.speed)
        E1.set_speed(self.speed)

        while self.playing:

            self.check_events()

            self.bg_summer.scroll(self.screen, self.speed)

            P1.move(self.screen)
            E1.move(self.screen)

            if self.game_state == "PAUSED":
                if self.close_button.draw(self.screen):
                    self.playing = False
                if self.back_button.draw(self.screen):
                    self.game_state = "GAME"

            self.window.blit(self.screen, (0, 0))
            pg.display.update()
            self.frame_per_second.tick(self.FPS)
            self.reset_keys()
            if not self.playing:
                pg.time.delay(500)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running, self.playing = False, False
                self.main_menu.run_display = False
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_a, pg.K_LEFT] and self.player_car_1.rect[0] != 450:
                    self.player_car_1.rect = self.player_car_1.rect.move([-300, 0])
                if event.key in [pg.K_d, pg.K_RIGHT] and self.player_car_1.rect[0] != 750:
                    self.player_car_1.rect = self.player_car_1.rect.move([300, 0])
                if event.key == pg.K_ESCAPE:
                    if self.game_state == "PAUSED":
                        self.game_state = "GAME"
                    else:
                        self.game_state = "PAUSED"

    def reset_keys(self):
        self.screen = pg.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def draw_text(self, text, size, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
