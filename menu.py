import pygame as pg
from game import Game
from utilities import Picture


class Menu(Game):
    cursor = pg.image.load().convert_alpha()

    def __init__(self):
        self.MIDDLE_WIDTH, self.MIDDLE_HEIGHT = self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT
        self.run_display = True
        self.cursor_rect = self.cursor.get_rect()
        self.cursor = Picture("images/cursor.png").image_rect
        self.offset = -100

    def draw_cursor(self):
        self.draw_text('*', 15, self.cursor_x, self.cursor.y)

    def blit_screen(self):
        self.window.blit(self.screen, (0, 0))
        pg.display.update()
        self.reset_keys()


class MainMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self.state = "START"
        self.start_x, self.start_y = self.MIDDLE_WIDTH, self.MIDDLE_HEIGHT + 30

        self.credits = "GARAGE"
        self.credits_x, self.credits_y = self.MIDDLE_WIDTH, self.MIDDLE_HEIGHT + 50

        self.options = "OPTIONS"
        self.options_x, self.options_y = self.MIDDLE_WIDTH, self.MIDDLE_HEIGHT + 70

        self.credits = "CREDITS"
        self.credits_x, self.credits_y = self.MIDDLE_WIDTH, self.MIDDLE_HEIGHT + 90








