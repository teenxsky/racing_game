import pygame as pg
from objects import Button, Picture


class Menu:
    def __init__(self, game):
        pg.init()
        self.game = game
        self.run_menu = True

    def blit_screen(self):
        self.game.window.blit(self.game.screen, (0, 0))
        pg.display.update()
        self.game.frame_per_second.tick(self.game.FPS)
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = None

    def display_menu(self):
        pg.display.set_caption("00 Racing")

        self.run_menu = True
        while self.run_menu:

            self.check_events()

            self.game.title_picture.draw_with_pulse(self.game.screen, 15)

            if self.game.start_button.draw(self.game.screen):
                self.state = "START"
                self.game.game_state = "GAME"
            if self.game.garage_button.draw(self.game.screen):
                self.state = "GARAGE"
            if self.game.music_button.draw(self.game.screen):
                self.state = "MUSIC"
            if self.game.sets_button.draw(self.game.screen):
                self.state = "SETS"
            if self.game.quit_button.draw(self.game.screen):
                self.game.running, self.game.playing, self.run_menu = False, False, False

            self.check_input()

            self.blit_screen()

            if not self.run_menu:
                pg.time.delay(500)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running, self.game.playing = False, False
                self.run_menu = False

    def check_input(self):
        if self.state == "START" and self.run_menu:
            self.game.playing = True
            self.run_menu = False
        elif self.state == "GARAGE":
            pass
        elif self.state == "MUSIC":
            pass
        elif self.state == "SETS":
            pass
        self.state = None



'''
class SetsMenu(Menu):
    def __init__(self, game):
        Menu.__init.(self, game)
        self.state = None

    def display_menu(self):
        self.run_display = True
        while self.run_display:
'''



