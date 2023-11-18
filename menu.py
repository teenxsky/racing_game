import pygame as pg
from objects import Button, Picture


class Menu:
    def __init__(self, game):
        pg.init()
        self.game = game
        self.run_display = True

    def blit_screen(self):
        self.game.window.blit(self.game.screen, (0, 0))
        self.game.frame_per_second.tick(self.game.FPS)
        pg.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = None

        button_sound = pg.mixer.Sound("audio/button_sound.mp3")



    def display_menu(self):

        self.run_display = True
        pg.display.set_caption("menu")

        while self.run_display:

            self.game.screen.fill('white')
            self.game.check_events()
            self.check_input()

            self.game.title_picture.draw_with_pulse(self.game.screen, 15)

            if self.game.start_button.draw(self.game.screen):
                self.state = "START"
            if self.game.garage_button.draw(self.game.screen):
                self.state = "GARAGE"
            if self.game.music_button.draw(self.game.screen):
                self.state = "MUSIC"
            if self.game.sets_button.draw(self.game.screen):
                self.state = "SETS"
            if self.game.quit_button.draw(self.game.screen):
                self.game.running, self.game.playing, self.run_display = False, False, False

            self.blit_screen()

    def check_input(self):
        if self.state == "START":
            self.game.playing = True
            self.run_display = False
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



