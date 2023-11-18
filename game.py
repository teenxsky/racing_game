import pygame as pg
from menu import MainMenu
from objects import Button, Picture


class Game:
    def __init__(self):
        pg.init()
        self.running, self.playing = True, False
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 720
        self.screen = pg.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.window = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.FPS = 30
        self.font_name = "fonts/pixfont.ttf"
        self.frame_per_second = pg.time.Clock()

        self.main_menu = MainMenu(self)

    def game_loop(self):
        pg.display.set_caption("gameloop")
        while self.playing:
            self.check_events()

            self.screen.fill('black')
            self.window.blit(self.screen, (0, 0))

            pg.display.update()
            self.frame_per_second.tick(self.FPS)
            self.reset_keys()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running, self.playing = False, False
                self.main_menu.run_display = False

    def reset_keys(self):
        self.screen = pg.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def draw_text(self, text, size, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
