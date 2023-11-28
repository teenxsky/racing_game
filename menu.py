import pygame.mouse

from objects import *
from settings import *


class Menu:
    def __init__(self, game):
        self.game = game

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running, self.game.playing = False, False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.game.keys["MOUSEBUTTONDOWN"] = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.keys["K_ESCAPE"] = True

    def blit_screen(self):
        for button in self.game.keys.keys():
            self.game.keys[button] = False

        self.game.window.blit(self.game.screen, (0, 0))
        pg.display.update()
        self.game.frame_per_second.tick(self.game.FPS)
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

        self.menu_bg = Background("images/backgrounds/background3.png", 1.25)
        self.menu_bg.resize(game.SCREEN_WIDTH, game.SCREEN_HEIGHT)
        self.title_picture = Picture(640, 150, "images/title_name.png", 1)

        button_sound = pg.mixer.Sound("audio/button_sound.mp3")
        self.start_button = Button(500, 277, "images/buttons/start_button_off.png", "images/buttons/start_button_on.png", button_sound, 0.3)
        self.garage_button = Button(780, 277, "images/buttons/garage_button_off.png", "images/buttons/garage_button_on.png", button_sound, 0.3)
        self.music_button = Button(500, 397, "images/buttons/music_button_off.png", "images/buttons/music_button_on.png", button_sound, 0.3)
        self.sets_button = Button(780, 397, "images/buttons/settings_button_off.png", "images/buttons/settings_button_on.png", button_sound, 0.3)
        self.quit_button = Button(640, 517, "images/buttons/quit_button_off.png", "images/buttons/quit_button_on.png", button_sound, 0.3)

        self.block = False

    def display_menu(self):

        self.game.menu_state = "MENU"
        while self.game.running and not self.game.playing:

            self.check_events()

            self.game.screen.blit(self.menu_bg.image, (0, 0))

            self.title_picture.draw_with_pulse(self.game.screen, 15)

            games = Text(640, 650, f'Hello, {settings.name}!', 40)
            games.draw(self.game.screen)

            if self.start_button.draw(self.game.screen, self.block) and self.game.keys["MOUSEBUTTONDOWN"]:
                self.game.menu_state = "START"
            if self.garage_button.draw(self.game.screen, self.block) and self.game.keys["MOUSEBUTTONDOWN"]:
                self.game.menu_state = "GARAGE"
            if self.music_button.draw(self.game.screen, self.block) and self.game.keys["MOUSEBUTTONDOWN"]:
                self.game.menu_state = "MUSIC"
            if self.sets_button.draw(self.game.screen, self.block) and self.game.keys["MOUSEBUTTONDOWN"]:
                self.game.menu_state = "SETS"
            if self.quit_button.draw(self.game.screen, self.block) and self.game.keys["MOUSEBUTTONDOWN"]:
                self.game.running, self.game.playing = False, False

            self.check_input()
            print(self.game.speed)

            self.blit_screen()

        pg.time.delay(500)

    def check_input(self):
        if self.game.menu_state == "START":
            self.game.playing = True
        elif self.game.menu_state == "GARAGE":
            self.game.garage_menu.display_menu()
        elif self.game.menu_state == "MUSIC":
            pass
        elif self.game.menu_state == "SETS":
            self.game.sets_menu.display_menu()
            self.block = True
        else:
            self.block = False


class SetsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

        button_sound = pg.mixer.Sound("audio/button_sound.mp3")
        self.sets_bg = Picture(640, 360, "images/backgrounds/sets_bg11.png", 0.5)
        self.sets_close_button = Button(390, 180, "images/buttons/close_button_off.png", "images/buttons/close_button_on.png", button_sound, 0.25)
        self.sets_back_button = Button(390, 270, "images/buttons/back_button_off.png", "images/buttons/back_button_on.png", button_sound, 0.25)
        self.sets_volume_button = Button(500, 300, "images/buttons/volume_button_off.png", "images/buttons/volume_button_on.png", button_sound, 0.25)
        self.sets_controls_button = Button(700, 300, "images/buttons/controls_button_off.png", "images/buttons/controls_button_on.png", button_sound, 0.25)
        self.text_volume = Text(640, 230, "VOLUME", 50)
        self.text_controls = Text(640, 230, "CONTROLS", 50)

        self.sub_state = "SETS"

    def display_menu(self):
        self.game.screen.blit(self.sets_bg.image, self.sets_bg.rect)

        if self.sub_state == "SETS":
            self.display_sets()
        elif self.sub_state == "CONTROLS":
            self.display_controls()
        elif self.sub_state == "VOLUME":
            self.display_volume()

        if self.sets_close_button.draw(self.game.screen, False) and self.game.keys["MOUSEBUTTONDOWN"]:
            self.game.menu_state = "MENU"
            self.sub_state = "SETS"

    def display_sets(self):

        if self.sets_controls_button.draw(self.game.screen, False) and self.game.keys["MOUSEBUTTONDOWN"]:
            self.sub_state = "CONTROLS"
        if self.sets_volume_button.draw(self.game.screen, False) and self.game.keys["MOUSEBUTTONDOWN"]:
            self.sub_state = "VOLUME"

        if self.game.keys["K_ESCAPE"]:
            self.game.menu_state = "MENU"
            self.sub_state = "SETS"

    def display_controls(self):
        self.text_controls.draw(self.game.screen)

        if self.game.keys["K_ESCAPE"] or (self.sets_back_button.draw(self.game.screen, False) and self.game.keys["MOUSEBUTTONDOWN"]):
            self.sub_state = "SETS"

    def display_volume(self):
        self.text_volume.draw(self.game.screen)

        if self.game.keys["K_ESCAPE"] or (self.sets_back_button.draw(self.game.screen, False) and self.game.keys["MOUSEBUTTONDOWN"]):
            self.sub_state = "SETS"


class GarageMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.garage_bg = Picture(640, 360, "images/backgrounds/garage_bg.jpeg")
        self.garage_bg.resize(game.SCREEN_WIDTH, game.SCREEN_HEIGHT)

        button_sound = pg.mixer.Sound("audio/button_sound.mp3")
        self.garage_close_button = Button(100, 100, "images/buttons/close_button_off.png", "images/buttons/close_button_on.png", button_sound, 0.25)

        self.yellow_car = Button(250, 600, "images/cars/yellow_car_off.png", "images/cars/yellow_car_on.png", button_sound, 0.6)
        self.white_car = Button(850, 600, "images/cars/white_car_off.png", "images/cars/white_car_on.png", button_sound, 0.6)

    def display_menu(self):

        while self.game.menu_state == "GARAGE":
            self.check_events()
            self.game.screen.blit(self.garage_bg.image, self.garage_bg.rect)

            if self.yellow_car.draw(self.game.screen, False) and self.game.keys["MOUSEBUTTONDOWN"]:
                settings.car = 3
            if self.white_car.draw(self.game.screen, False) and self.game.keys["MOUSEBUTTONDOWN"]:
                settings.car = 2

            if self.game.keys["K_ESCAPE"] or (self.garage_close_button.draw(self.game.screen, False) and self.game.keys["MOUSEBUTTONDOWN"]):
                self.game.menu_state = "MENU"

            self.blit_screen()

        # pg.time.delay(500)
