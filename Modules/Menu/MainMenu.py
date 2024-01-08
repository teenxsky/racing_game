from .Menu import *
from Modules.Objects.GUIObjects.Text import Text
import getpass


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

        self.title_picture = Picture("Resources/Images/title_name.png", 0.95)

        self.start_button = Button("Resources/Images/Buttons/start_button_off.png",
                                   "Resources/Images/Buttons/start_button_on.png", button_sound, 0.3)
        self.garage_button = Button("Resources/Images/Buttons/garage_button_off.png",
                                    "Resources/Images/Buttons/garage_button_on.png", button_sound, 0.3)
        self.music_button = Button("Resources/Images/Buttons/music_button_off.png",
                                   "Resources/Images/Buttons/music_button_on.png", button_sound, 0.3)
        self.quit_button = Button("Resources/Images/Buttons/quit_button_off.png",
                                  "Resources/Images/Buttons/quit_button_on.png",
                                  button_sound, 0.25)

        self.sets_button = Button("Resources/Images/Buttons/default_button_off.png",
                                  "Resources/Images/Buttons/default_button_on.png", button_sound, 0.115)

        self.authors_button = Button("Resources/Images/Buttons/authors_button_off.png",
                                     "Resources/Images/Buttons/authors_button_on.png", button_sound, 0.115)

        self.copyright_text = Text("© 2023-2024 00Team, All rights reserved", 12)

        if not settings.player_stats["name"]:
            settings.player_stats["name"] = getpass.getuser()

        self.song_number = 0
        self.last_update = pg.time.get_ticks()

        self.menu_bg, self.menu_bg_speed = None, None
        self.bg_sound = None

        self.block = False

    def display_menu(self):
        self.menu_bg, self.menu_bg_speed = load_bg("menu_bg")

        self.game.menu_state = "MENU"

        self.bg_sound = load_bg_sound("menu_bg")

        while self.game.running and not self.game.playing:
            self.check_events()

            self.menu_bg.draw(self.game.screen, self.menu_bg_speed)
            self.title_picture.draw_with_pulse(self.game.screen, (640, 90), size=10, time=100)

            if not self.bg_sound.num_channels:
                self.bg_sound.play(loops=-1, fade_ms=500)

            if self.start_button.draw(self.game.screen, (20, 240), self.block, position="midleft") and self.game.keys[
                    "MOUSE DOWN"]:
                self.game.menu_state = "LEVELS"
                self.last_update = pg.time.get_ticks()
            if self.garage_button.draw(self.game.screen, (20, self.start_button.rect.bottomleft[1] + 25), self.block,
                                       position="topleft") and self.game.keys["MOUSE DOWN"]:
                self.game.menu_state = "GARAGE"
                self.last_update = pg.time.get_ticks()
            if self.music_button.draw(self.game.screen, (20, self.garage_button.rect.bottomleft[1] + 25), self.block,
                                      position="topleft") and self.game.keys["MOUSE DOWN"]:
                self.game.menu_state = "MUSIC"
            if self.quit_button.draw(self.game.screen, (20, self.music_button.rect.bottomleft[1] + 25), self.block,
                                     position="topleft") and self.game.keys["MOUSE DOWN"]:
                self.game.running, self.game.playing = False, False
                self.game.garage_menu.player_stats.update_time_in_game()
                self.game.music_player.clean_covers()

            self.copyright_text.draw(self.game.screen, (20, 700), position="bottomleft")

            if self.sets_button.draw(self.game.screen, (1260, 700), self.block, position="bottomright") and \
                    self.game.keys["MOUSE DOWN"]:
                self.game.menu_state = "SETS"
            if self.authors_button.draw(self.game.screen, (1202, 700), self.block, position="bottomright") and \
                    self.game.keys["MOUSE DOWN"]:
                self.game.menu_state = "AUTHORS"

            self.game.music_player.draw_current_song(self.game.screen, (1260, 630), position="bottomright", text_up=True, game=self.game, block=self.block)

            self.display_mission()

            user_name = Text(f'Hello, {settings.player_stats["name"]}!', 35)
            user_name.draw(self.game.screen, (640, self.authors_button.rect.centery))

            self.check_input()
            self.game.blit_screen()

        pg.time.delay(500)
        pg.mixer.fadeout(500)

    def display_mission(self):
        bar = pg.Surface((295, 335), pg.SRCALPHA).convert_alpha()
        bar.fill((0, 0, 0, 125))
        bar_rect = bar.get_rect()

        missions_text = Text("MISSIONS", 40)
        missions_text.draw(bar, (bar_rect.width // 2, 10), position="midtop")

        bar_rect.topright = (1260, self.start_button.rect.topright[1])
        self.game.screen.blit(bar, bar_rect)

    def check_input(self):
        self.block = self.game.menu_state == "MUSIC" \
                     or self.game.menu_state == "SETS" or self.game.menu_state == "AUTHORS"

        if self.game.menu_state == "LEVELS":
            self.game.blit_screen()
            self.bg_sound.stop(fadeout=500)
            # pg.time.delay(250)
            self.game.transition = True
            if delay(self.last_update):
                self.game.levels_menu.display_menu()

        if self.game.menu_state == "START":
            self.game.playing = True

        if self.game.menu_state == "GARAGE":
            self.game.blit_screen()
            self.bg_sound.stop(fadeout=500)
            # pg.time.delay(500)
            self.game.transition = True
            if delay(self.last_update):
                self.game.garage_menu.display_menu()

        if self.game.menu_state == "MUSIC":
            self.game.music_menu.display_menu()

        if self.game.menu_state == "SETS":
            self.game.sets_menu.display_menu()

        if self.game.menu_state == "AUTHORS":
            self.game.authors_menu.display_menu()
