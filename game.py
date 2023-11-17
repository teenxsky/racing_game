import pygame as pg
from button import Button


class Game:
    def __init__(self):
        pg.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 720
        self.screen = pg.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.window = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.font_name = "fonts/pixfont.ttf"
        self.frame_per_second = pg.time.Clock()

    def game_loop(self):
        button_sound = pg.mixer.Sound("audio/button_sound.mp3")

        start_but_off = pg.image.load("images/buttons/start_button_off.png").convert_alpha()
        start_but_on = pg.image.load("images/buttons/start_button_on.png").convert_alpha()
        start_button = Button(100, 80, start_but_off, start_but_on, button_sound, 0.3)

        garage_but_off = pg.image.load("images/buttons/garage_button_off.png").convert_alpha()
        garage_but_on = pg.image.load("images/buttons/garage_button_on.png").convert_alpha()
        garage_button = Button(100, 200, garage_but_off, garage_but_on, button_sound, 0.3)

        music_but_off = pg.image.load("images/buttons/music_button_off.png").convert_alpha()
        music_but_on = pg.image.load("images/buttons/music_button_on.png").convert_alpha()
        music_button = Button(100, 320, music_but_off, music_but_on, button_sound, 0.3)

        sets_but_off = pg.image.load("images/buttons/settings_button_off.png").convert_alpha()
        sets_but_on = pg.image.load("images/buttons/settings_button_on.png").convert_alpha()
        sets_button = Button(100, 440, sets_but_off, sets_but_on, button_sound, 0.3)

        quit_but_off = pg.image.load("images/buttons/quit_button_off.png").convert_alpha()
        quit_but_on = pg.image.load("images/buttons/quit_button_on.png").convert_alpha()
        quit_button = Button(100, 560, quit_but_off, quit_but_on, button_sound, 0.3)
        FPS = 30

        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.screen.fill((0, 0, 0))
            self.draw_text('XUESOS', 20, self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
            self.window.blit(self.screen, (0, 0))

            start_button.draw(self.window)
            garage_button.draw(self.window)
            music_button.draw(self. window)
            sets_button.draw(self.window)
            quit_button.draw(self.window)

            pg.display.update()
            self.frame_per_second.tick(FPS)
            self.reset_keys()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running, self.playing = False, False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.START_KEY = True
                elif event.key == pg.K_BACKSPACE:
                    self.BACK_KEY = True
                elif event.key == pg.K_UP:
                    self.UP_KEY = True
                elif event.key == pg.K_DOWN:
                    self.DOWN_KEY = True

    def reset_keys(self):
        self.screen = pg.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def draw_text(self, text, size, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)


