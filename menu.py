from objects import *


class Menu:
    def __init__(self, game):
        pg.init()
        self.game = game
        self.run_menu = True
        self.keys = None
        self.clicked = False

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running, self.game.playing = False, False
                self.run_menu = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked = True

        self.keys = pg.key.get_pressed()

    def blit_screen(self):
        self.clicked = False

        self.game.window.blit(self.game.screen, (0, 0))
        pg.display.update()
        self.game.frame_per_second.tick(self.game.FPS)
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "MENU"
        self.run_menu = True
        self.block = False

    def display_menu(self):
        pg.display.set_caption("00 Racing")

        self.run_menu = True
        while self.run_menu:

            self.check_events()

            self.game.screen.blit(self.game.menu_bg.image, (0, 0))

            self.game.title_picture.draw_with_pulse(self.game.screen, 15)

            if self.game.start_button.draw(self.game.screen, self.block) and self.clicked:
                self.state = "START"
            if self.game.garage_button.draw(self.game.screen, self.block) and self.clicked:
                self.state = "GARAGE"
            if self.game.music_button.draw(self.game.screen, self.block) and self.clicked:
                self.state = "MUSIC"
            if self.game.sets_button.draw(self.game.screen, self.block) and self.clicked:
                self.state = "SETS"
                self.game.sets_menu.run_sets = True
            if self.game.quit_button.draw(self.game.screen, self.block) and self.clicked:
                self.game.running, self.game.playing = False, False
                self.run_menu, self.game.sets_menu = False, False

            self.check_input()

            self.blit_screen()

        pg.time.delay(500)

    def check_input(self):
        if self.state == "START":
            self.state = "MENU"
            self.game.game_state = "GAME"
            self.game.playing = True
            self.run_menu = False
        elif self.state == "GARAGE":
            pass
        elif self.state == "MUSIC":
            pass
        elif self.state == "SETS":
            self.game.sets_menu.display_menu()


class SetsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "SETS"
        self.text_volume = Text(640, 230, "VOLUME", 50)
        self.text_controls = Text(640, 230, "CONTROLS", 50)

        self.keys = self.game.main_menu.keys

    def display_menu(self):
        self.game.screen.blit(self.game.sets_bg.image, self.game.sets_bg.rect)
        self.game.main_menu.block = True

        if self.state == "SETS":
            self.display_sets()
        if self.state == "VOLUME":
            self.display_volume()
        if self.state == "CONTROLS":
            self.display_controls()

        if self.game.sets_close_button.draw(self.game.screen, False) and self.game.main_menu.clicked:
            self.game.main_menu.block = False
            self.game.main_menu.state = "MENU"
            self.state = "SETS"

    def display_sets(self):
        keys = self.game.main_menu.keys

        if self.game.sets_controls_button.draw(self.game.screen, False) and self.game.main_menu.clicked:
            self.state = "CONTROLS"
        if self.game.sets_volume_button.draw(self.game.screen, False) and self.game.main_menu.clicked:
            self.state = "VOLUME"

        # if keys[pg.K_ESCAPE]:  ЗАВЕСТИ СЛОВАРЬ С НАЖАТЫМИ КЛАВИШАМИ КАК КЛЮЧИ И ЗАНЧЕНИЯМИ БУДУТ FALSE or TRUE
        #    self.game.main_menu.block = False
        #    self.game.main_menu.state = "MENU"


    def display_volume(self):
        keys = self.game.main_menu.keys

        self.text_volume.draw(self.game.screen)

        if keys[pg.K_ESCAPE] or (self.game.sets_back_button.draw(self.game.screen, False) and self.game.main_menu.clicked):
            self.state = "SETS"

    def display_controls(self):
        keys = self.game.main_menu.keys

        self.text_controls.draw(self.game.screen)

        if keys[pg.K_ESCAPE] or (self.game.sets_back_button.draw(self.game.screen, False) and self.game.main_menu.clicked):
            self.state = "SETS"

# class MusicMenu:


'''
class SetsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.run_sets = None
        self.state = None

    def display_menu(self):
        
        self.run_sets = True

        while self.run_sets:
            self.check_events()

            self.game.screen.blit(self.game.sets_bg.image, self.game.sets_bg.rect)

            self.game.window.blit(self.game.screen, (0, 0))
            pg.display.update()
            self.game.frame_per_second.tick(self.game.FPS)
            self.check_input()
            print('sets')

    def check_input(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.curr_menu = self.game.main_menu
                    self.run_sets = False
'''
