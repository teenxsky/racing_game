import pygame as pg
from menu import MainMenu
from objects import Button, Picture

pg.init()


class Game:
    def __init__(self):
        pg.init()
        self.running, self.playing = True, False
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 720
        self.clicked = False
        self.screen = pg.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.window = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.FPS = 60
        self.font_name = "fonts/pixfont.ttf"
        self.frame_per_second = pg.time.Clock()

        self.main_menu = MainMenu(self)
        button_sound = pg.mixer.Sound("audio/button_sound.mp3")

        game_background = pg.image.load("images/summer_road.png").convert_alpha()
        self.game_background = Picture(0, 0, game_background)
        self.game_background.resize(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        start_but_off = pg.image.load("images/buttons/start_button_off.png").convert_alpha()
        start_but_on = pg.image.load("images/buttons/start_button_on.png").convert_alpha()
        self.start_button = Button(100, 70, start_but_off, start_but_on, button_sound, 0.3)

        garage_but_off = pg.image.load("images/buttons/garage_button_off.png").convert_alpha()
        garage_but_on = pg.image.load("images/buttons/garage_button_on.png").convert_alpha()
        self.garage_button = Button(100, 190, garage_but_off, garage_but_on, button_sound, 0.3)

        music_but_off = pg.image.load("images/buttons/music_button_off.png").convert_alpha()
        music_but_on = pg.image.load("images/buttons/music_button_on.png").convert_alpha()
        self.music_button = Button(100, 310, music_but_off, music_but_on, button_sound, 0.3)

        sets_but_off = pg.image.load("images/buttons/settings_button_off.png").convert_alpha()
        sets_but_on = pg.image.load("images/buttons/settings_button_on.png").convert_alpha()
        self.sets_button = Button(100, 430, sets_but_off, sets_but_on, button_sound, 0.3)

        quit_but_off = pg.image.load("images/buttons/quit_button_off.png").convert_alpha()
        quit_but_on = pg.image.load("images/buttons/quit_button_on.png").convert_alpha()
        self.quit_button = Button(100, 550, quit_but_off, quit_but_on, button_sound, 0.3)

        title_image = pg.image.load("images/title_name.png")
        self.title_picture = Picture(400, 15, title_image, 0.5)

        close_but_off = pg.image.load("images/buttons/close_button_off.png").convert_alpha()
        close_but_on = pg.image.load("images/buttons/close_button_on.png").convert_alpha()
        self.close_button = Button(550, 300, close_but_off, close_but_on, button_sound, 0.25)

        back_but_off = pg.image.load("images/buttons/back_button_off.png").convert_alpha()
        back_but_on = pg.image.load("images/buttons/back_button_on.png").convert_alpha()
        self.back_button = Button(670, 300, back_but_off, back_but_on, button_sound, 0.25)

        self.game_state = "GAME"

    def game_loop(self):
        pg.display.set_caption("gameloop")
        self.game_state = "GAME"

        while self.playing:
            self.check_events()

            self.window.blit(self.game_background.image, (0, 0))

            if self.game_state == "PAUSE":
                if self.close_button.draw(self.window):
                    self.playing = False
                if self.back_button.draw(self.window):
                    self.game_state = "GAME"

            pg.display.update()
            self.frame_per_second.tick(self.FPS)
            self.reset_keys()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running, self.playing = False, False
                self.main_menu.run_display = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.game_state == "PAUSE":
                        self.game_state = "GAME"
                    else:
                        self.game_state = "PAUSE"

    def reset_keys(self):
        self.screen = pg.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def draw_text(self, text, size, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
