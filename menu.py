from objects import *
from settings import *


class Menu:
    def __init__(self, game):
        self.game = game
        self.hud = HUD()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running, self.game.playing = False, False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.game.keys["MOUSEBUTTONDOWN"] = True
            if event.type == pg.KEYDOWN:
                print(pg.key.name(event.key), event.key)
                if event.key == settings.KEYS["BACK"]:

                    self.game.keys["BACK"] = True

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

            self.title_picture.draw_with_pulse(self.game.screen)

            games = Text(640, 650, f'Hello, {settings.name}!', 40)
            games.draw(self.game.screen)

            self.hud.draw_coins(self.game.screen, 100, 400, 250)

            if self.start_button.draw(self.game.screen, self.block) and self.game.keys["MOUSEBUTTONDOWN"]:
                self.game.menu_state = "START"
            if self.garage_button.draw(self.game.screen, self.block) and self.game.keys["MOUSEBUTTONDOWN"]:
                self.game.menu_state = "GARAGE"
            if self.music_button.draw(self.game.screen, self.block) and self.game.keys["MOUSEBUTTONDOWN"]:
                self.game.menu_state = "MUSIC"
                settings.coins += 1
            if self.sets_button.draw(self.game.screen, self.block) and self.game.keys["MOUSEBUTTONDOWN"]:
                self.game.menu_state = "SETS"
            if self.quit_button.draw(self.game.screen, self.block) and self.game.keys["MOUSEBUTTONDOWN"]:
                self.game.running, self.game.playing = False, False

            self.check_input()

            self.blit_screen()

        pg.time.delay(500)

    def check_input(self):
        if self.game.menu_state == "START":
            self.game.playing = True
        elif self.game.menu_state == "GARAGE":
            pg.time.delay(500)
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
        self.sets_bg = Picture(640, 360, "images/backgrounds/window_2.png", 0.5)
        self.sets_close_button = Button(860, 230, "images/buttons/close_button_off.png", "images/buttons/close_button_on.png", button_sound, 0.25)
        self.sets_back_button = Button(420, 230, "images/buttons/back_button_off.png", "images/buttons/back_button_on.png", button_sound, 0.25)

        self.sets_volume_button = Button(420, 330, "images/buttons/volume_button_off.png", "images/buttons/volume_button_on.png", button_sound, 0.25)
        self.text_volume_sub = Text(*self.sets_volume_button.rect_on.midright, "VOLUME", 40, button_sound)
        self.text_volume_sub.rect.x += self.text_volume_sub.rect.width / 2 + 20

        self.sets_controls_button = Button(420, 440, "images/buttons/controls_button_off.png", "images/buttons/controls_button_on.png", button_sound, 0.25)
        self.text_controls_sub = Text(*self.sets_controls_button.rect_on.midright, "CONTROLS", 40, button_sound)
        self.text_controls_sub.rect.x += self.text_controls_sub.rect.width / 2 + 20

        self.text_volume = Text(640, 230, "VOLUME", 50, button_sound)
        self.text_controls = Text(640, 230, "CONTROLS", 50, button_sound)

        distance = 0
        self.text_keys = []
        for key in settings.KEYS.keys():
            self.text_keys.append(Text(640, 290 + distance, key, 30, button_sound))
            distance += 30

        self.sub_state = "SETS"
        self.sub_block = True

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
        if self.sets_controls_button.draw(self.game.screen, False):
            self.text_controls_sub.draw(self.game.screen)
            if self.game.keys["MOUSEBUTTONDOWN"]:
                self.sub_state = "CONTROLS"
        if self.sets_volume_button.draw(self.game.screen, False):
            self.text_volume_sub.draw(self.game.screen)
            if self.game.keys["MOUSEBUTTONDOWN"]:
                self.sub_state = "VOLUME"

        if self.game.keys["BACK"]:
            self.game.menu_state = "MENU"
            self.sub_state = "SETS"

    def display_controls(self):
        self.text_controls.draw(self.game.screen)

        for key in self.text_keys:
            if key.draw_as_button(self.game.screen):
                self.button_choosing(key, key.string)

        if self.game.keys["BACK"] or (self.sets_back_button.draw(self.game.screen, False) and self.game.keys["MOUSEBUTTONDOWN"]):
            self.sub_state = "SETS"

    def button_choosing(self, button, button_name):
        chosen = False
        curr_button = Text(*button.rect.midright, pg.key.name(settings.KEYS[button_name]), button.scale)
        curr_button.rect.x += curr_button.rect.width / 2 + 15
        curr_button.draw(self.game.screen)

        if self.game.keys["MOUSEBUTTONDOWN"]:
            while not chosen:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.game.running, self.game.playing = False, False
                        pg.quit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.game.keys["MOUSEBUTTONDOWN"] = True
                    if event.type == pg.KEYDOWN:
                        if event.key not in settings.KEYS.values() \
                                or settings.KEYS[button_name] == event.key:
                            settings.KEYS[button_name] = event.key
                            chosen = True

                for button in self.game.keys.keys():
                    self.game.keys[button] = False
                pg.display.update()
                self.game.frame_per_second.tick(self.game.FPS)

    def display_volume(self):
        self.text_volume.draw(self.game.screen)

        if self.game.keys["BACK"] or (self.sets_back_button.draw(self.game.screen, False) and self.game.keys["MOUSEBUTTONDOWN"]):
            self.sub_state = "SETS"


class GarageMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.garage_bg = Picture(640, 360, "images/backgrounds/garage_bg.jpeg")
        self.garage_bg.resize(game.SCREEN_WIDTH, game.SCREEN_HEIGHT)

        button_sound = pg.mixer.Sound("audio/button_sound.mp3")
        self.garage_close_button = Button(100, 100, "images/buttons/close_button_off.png", "images/buttons/close_button_on.png", button_sound, 0.25)

        self.yellow_car = Picture(250, 600, "images/cars/yellow_car_off.png", 0.6)

        self.white_car = Picture(850, 550, "images/cars/white_car_off.png", 1)

    def display_menu(self):

        while self.game.menu_state == "GARAGE":
            self.check_events()
            self.game.screen.blit(self.garage_bg.image, self.garage_bg.rect)

            text_curr_car = Text(640, 100, f'Your car: {settings.car}', 20)
            text_curr_car.draw(self.game.screen)

            if self.yellow_car.draw(self.game.screen):
                self.yellow_car.draw_with_pulse(self.game.screen)
                if self.game.keys["MOUSEBUTTONDOWN"]:
                    settings.car = 3
            if self.white_car.draw(self.game.screen):
                self.white_car.draw_with_pulse(self.game.screen)

                if self.game.keys["MOUSEBUTTONDOWN"]:
                    settings.car = 2

            if self.game.keys["BACK"] or (self.garage_close_button.draw(self.game.screen, False) and self.game.keys["MOUSEBUTTONDOWN"]):
                self.game.menu_state = "MENU"

            self.blit_screen()

        pg.time.delay(500)


#class MusicMenu(Menu):

