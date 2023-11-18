import pygame as pg
from objects import Button, Picture


class Menu:
    def __init__(self, game):
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

    def display_menu(self):
        button_sound = pg.mixer.Sound("audio/button_sound.mp3")

        start_but_off = pg.image.load("images/buttons/start_button_off.png").convert_alpha()
        start_but_on = pg.image.load("images/buttons/start_button_on.png").convert_alpha()
        start_button = Button(100, 70, start_but_off, start_but_on, button_sound, 0.3)

        garage_but_off = pg.image.load("images/buttons/garage_button_off.png").convert_alpha()
        garage_but_on = pg.image.load("images/buttons/garage_button_on.png").convert_alpha()
        garage_button = Button(100, 190, garage_but_off, garage_but_on, button_sound, 0.3)

        music_but_off = pg.image.load("images/buttons/music_button_off.png").convert_alpha()
        music_but_on = pg.image.load("images/buttons/music_button_on.png").convert_alpha()
        music_button = Button(100, 310, music_but_off, music_but_on, button_sound, 0.3)

        sets_but_off = pg.image.load("images/buttons/settings_button_off.png").convert_alpha()
        sets_but_on = pg.image.load("images/buttons/settings_button_on.png").convert_alpha()
        sets_button = Button(100, 430, sets_but_off, sets_but_on, button_sound, 0.3)

        quit_but_off = pg.image.load("images/buttons/quit_button_off.png").convert_alpha()
        quit_but_on = pg.image.load("images/buttons/quit_button_on.png").convert_alpha()
        quit_button = Button(100, 550, quit_but_off, quit_but_on, button_sound, 0.3)

        title_image = pg.image.load("images/title_name.png")
        title_picture = Picture(400, 15, title_image, 0.5)

        self.run_display = True
        pg.display.set_caption("menu")
        while self.run_display:

            self.game.screen.fill('white')
            self.game.check_events()
            self.check_input()

            title_picture.draw_with_pulse(self.game.screen, 15)

            if start_button.draw(self.game.screen):
                self.state = "START"
            if garage_button.draw(self.game.screen):
                self.state = "GARAGE"
            if music_button.draw(self.game.screen):
                self.state = "MUSIC"
            if sets_button.draw(self.game.screen):
                self.state = "SETS"
            if quit_button.draw(self.game.screen):
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

'''
class SetsMenu(Menu):
    def __init__(self, game):
        Menu.__init.(self, game)
        self.state = None

    def display_menu(self):
        self.run_display = True
        while self.run_display:
'''



