from objects import *
from settings import *
import webbrowser
import getpass

BLUE = (147, 179, 242)


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
                    self.game.keys["MOUSE DOWN"] = True
            if event.type == pg.KEYDOWN:
                if event.key == settings.KEYS["BACK"]:
                    self.game.keys["BACK"] = True
                if event.key == settings.KEYS["ENTER"]:
                    self.game.keys["ENTER"] = True
                if event.key == settings.KEYS["MOVE LEFT"]:
                    self.game.keys["MOVE LEFT"] = True
                if event.key == settings.KEYS["MOVE RIGHT"]:
                    self.game.keys["MOVE RIGHT"] = True
            if event.type == pg.MOUSEWHEEL:
                self.game.keys["MOUSEWHEEL"] = event.y
            if event.type == self.game.player.MUSIC_END:
                self.game.player.playing = False
                if self.game.player.loop:
                    self.game.player.play()
                else:
                    self.game.player.next()


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

        self.title_picture = Picture(640, 150, "images/title_name.png", 1)

        button_sound = pg.mixer.Sound("audio/button_sound.mp3")
        self.start_button = Button(500, 277, "images/buttons/start_button_off.png", "images/buttons/start_button_on.png", button_sound, 0.3)
        self.garage_button = Button(780, 277, "images/buttons/garage_button_off.png", "images/buttons/garage_button_on.png", button_sound, 0.3)
        self.music_button = Button(500, 397, "images/buttons/music_button_off.png", "images/buttons/music_button_on.png", button_sound, 0.3)
        self.sets_button = Button(780, 397, "images/buttons/settings_button_off.png", "images/buttons/settings_button_on.png", button_sound, 0.3)
        self.quit_button = Button(640, 517, "images/buttons/quit_button_off.png", "images/buttons/quit_button_on.png", button_sound, 0.3)

        self.levels_close_button = Button(40, 40, "images/buttons/close_button_off.png", "images/buttons/close_button_on.png", button_sound, 0.15)
        self.levels_start_button = Button(640, 580, "images/buttons/start_button_off.png", "images/buttons/start_button_on.png", button_sound, 0.2)
        self.levels_back_button = Button(290, 360, "images/buttons/back_button_off.png", "images/buttons/back_button_on.png", button_sound, 0.15)
        self.levels_forward_button = Button(990, 360, "images/buttons/forward_button_off.png", "images/buttons/forward_button_on.png", button_sound, 0.15)

        self.github_icon = Picture(1240, 680, "images/github.png", 0.02)

        self.block = False

    def display_menu(self):
        path = f'images/backgrounds/bgs/{settings.bg["menu_bg"]}/'
        menu_bg = GIF(path)
        menu_bg.resize(1280, 720)
        menu_bg_speed = settings.bg_speed[settings.bg["menu_bg"]]

        self.game.menu_state = "MENU"

        while self.game.running and not self.game.playing:
            self.check_events()

            menu_bg.draw(self.game.screen, menu_bg_speed)
            self.title_picture.draw_with_pulse(self.game.screen)

            user_name = Text(640, 650, f'Hello, {getpass.getuser()}!', 40)
            user_name.draw(self.game.screen)

            self.hud.draw_coins(self.game.screen, 100, 400, 250)

            if self.start_button.draw(self.game.screen, self.block) and self.game.keys["MOUSE DOWN"]:
                self.game.menu_state = "LEVELS"
            if self.garage_button.draw(self.game.screen, self.block) and self.game.keys["MOUSE DOWN"]:
                self.game.menu_state = "GARAGE"
            if self.music_button.draw(self.game.screen, self.block) and self.game.keys["MOUSE DOWN"]:
                self.game.menu_state = "MUSIC"
            if self.sets_button.draw(self.game.screen, self.block) and self.game.keys["MOUSE DOWN"]:
                self.game.menu_state = "SETS"
            if self.quit_button.draw(self.game.screen, self.block) and self.game.keys["MOUSE DOWN"]:
                self.game.running, self.game.playing = False, False

            if self.github_icon.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
                webbrowser.open("https://github.com/teenxsky/racing_game", new=0, autoraise=True)

            self.check_input()

            self.game.blit_screen()

        pg.time.delay(500)

    def display_levels(self):
        path = f'images/backgrounds/bgs/{settings.bg["levels_bg"]}/'
        levels_bg = GIF(path)
        levels_bg.resize(1280, 720)
        levels_bg_speed = settings.bg_speed[settings.bg["levels_bg"]]
        levels_gui_1 = Picture(640, 360, "images/backgrounds/levels_gui.png")
        levels_gui_1.resize(1280, 720)
        levels_gui_2 = Picture(640, 358, "images/backgrounds/window_trans.png")
        levels_gui_2.resize(595, 355)
        levels_text = Text(640, 40, "LEVELS", 40)

        levels = []
        for file in sorted(os.listdir("images/backgrounds/levels/")):
            try:
                preview = os.listdir("images/backgrounds/levels/" + file + "/")[1]
                if ".png" in preview:
                    levels.append(Picture(640, 360, "images/backgrounds/levels/" + file + "/" + preview, 5))
            except IndexError:
                pass
            except pygame.error:
                pass
            except NotADirectoryError:
                pass

        curr_lvl_x = 640
        while self.game.running and not self.game.playing and self.game.menu_state == "LEVELS":
            self.check_events()
            levels_bg.draw(self.game.screen, levels_bg_speed)
            levels_gui_1.draw(self.game.screen)
            levels_text.draw(self.game.screen)

            distance = 0
            for level in levels:
                center = (curr_lvl_x + distance, 360)
                level.rect.center = center
                levels_gui_2.rect.center = center
                level.draw(self.game.screen)
                if settings.levels[levels.index(level)]["access"]:
                    if level.rect.center == (640, 360):
                        if self.levels_start_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
                            self.game.menu_state = "START"
                else:
                    block = pg.surface.Surface((570, 320), pg.SRCALPHA)
                    block = block.convert_alpha()
                    block.fill((0, 0, 0, 200))
                    self.game.screen.blit(block, level.rect)
                levels_gui_2.draw(self.game.screen)
                c_1 = Text(center[0], 690, f'DIFFICULTY: {settings.levels[levels.index(level)]["difficulty"]}', 30)
                c_1.draw(self.game.screen)
                distance += 700
            distance -= 700

            self.game.curr_level = abs(curr_lvl_x + distance - 640) // 700

            if curr_lvl_x + 700 <= 640:
                if (self.levels_back_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]) or (self.game.keys["MOVE LEFT"]):
                    curr_lvl_x += 700

            if curr_lvl_x + distance - 700 >= 640:
                if (self.levels_forward_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]) or (self.game.keys["MOVE RIGHT"]):
                    curr_lvl_x -= 700

            if self.levels_close_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
                self.game.menu_state = "MENU"

            self.game.blit_screen()

    def check_input(self):
        self.block = self.game.menu_state == "MUSIC"\
                     or self.game.menu_state == "SETS"

        if self.game.menu_state == "LEVELS":
            self.display_levels()

        if self.game.menu_state == "START":
            self.game.playing = True

        if self.game.menu_state == "GARAGE":
            pg.time.delay(500)
            self.game.garage_menu.display_menu()

        if self.game.menu_state == "MUSIC":
            self.game.music_menu.display_menu()

        if self.game.menu_state == "SETS":
            self.game.sets_menu.display_menu()


class SetsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

        button_sound = pg.mixer.Sound("audio/button_sound.mp3")
        self.sets_bg = Picture(640, 360, "images/backgrounds/window.png", 0.5)
        self.sets_close_button = Button(865, 225, "images/buttons/close_button_off.png", "images/buttons/close_button_on.png", button_sound, 0.2)
        self.sets_back_button = Button(415, 225, "images/buttons/back_button_off.png", "images/buttons/back_button_on.png", button_sound, 0.2)

        self.text_settings = Text(640, 225, "SETTNGS", 45, button_sound)
        self.text_volume = Text(640, 225, "VOLUME", 45, button_sound)
        self.text_controls = Text(640, 225, "CONTROLS", 45, button_sound)

        self.sets_volume_button = Button(408, 467, "images/buttons/volume_button_off.png", "images/buttons/volume_button_on.png", button_sound, 0.15)
        self.sets_controls_button = Button(468, 467, "images/buttons/controls_button_off.png", "images/buttons/controls_button_on.png", button_sound, 0.15)
        self.sets_text = [Text(5, 5, "VOLUME", 32, set_topleft=True, color=BLUE),
                          Text(5, 5, "CONTROLS", 32, set_topleft=True, color=BLUE)
                          ]

        self.volume_text = [Text(10, 0, "GENERAL VOLUME", 28, set_topleft=True, color=BLUE),
                            Text(10, 0, "MUSIC VOLUME", 28, set_topleft=True, color=BLUE),
                            Text(10, 0, "SOUNDS VOLUME", 28, set_topleft=True, color=BLUE)
                            ]

        self.text_keys = []
        for key in settings.KEYS.keys():
            self.text_keys.append(Text(5, 0, key, 25, button_sound, set_topleft=True, color=BLUE))

        self.scroll_y = 0
        self.sub_state = "SETS"

    def display_menu(self):
        self.game.screen.blit(self.sets_bg.image, self.sets_bg.rect)

        if self.sub_state == "SETS":
            self.display_sets()
        elif self.sub_state == "CONTROLS":
            self.display_controls()
        elif self.sub_state == "VOLUME":
            self.display_volume()

        if self.sets_close_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
            self.game.menu_state = "MENU"
            self.sub_state = "SETS"

    def display_sets(self):
        self.text_settings.draw(self.game.screen)

        if self.sets_controls_button.draw(self.game.screen):
            if self.game.keys["MOUSE DOWN"]:
                self.sub_state = "CONTROLS"
        if self.sets_volume_button.draw(self.game.screen):
            if self.game.keys["MOUSE DOWN"]:
                self.sub_state = "VOLUME"

        bar = pg.surface.Surface((510, 170))
        bar.fill((162, 48, 42))
        bar_rect = bar.get_rect()
        bar_rect.center = (640, 350)

        distance = 0
        for text in self.sets_text:
            text.rect.y = self.scroll_y + distance
            if text.draw_as_button(bar, surface_topleft=bar_rect.topleft):
                if self.game.keys["MOUSE DOWN"]:
                    self.sub_state = text.string
            distance += 40

        if self.sets_text[0].rect.y + (self.game.keys["MOUSEWHEEL"] * 10) <= 0 \
                and self.sets_text[-1].rect.y + (self.game.keys["MOUSEWHEEL"] * 10) >= bar_rect.height:
            self.scroll_y += self.game.keys["MOUSEWHEEL"] * 10

        self.game.screen.blit(bar, bar_rect)
        if self.game.keys["BACK"]:
            self.game.menu_state = "MENU"
            self.sub_state = "SETS"
            self.scroll_y = 0

    def display_controls(self):
        self.text_controls.draw(self.game.screen)

        bar = pg.surface.Surface((510, 190))
        bar.fill((162, 48, 42))
        bar_rect = bar.get_rect()
        bar_rect.center = (640, 360)

        distance = 0
        for key in self.text_keys:
            key.rect.y = self.scroll_y + distance
            if key.draw_as_button(bar, surface_topleft=bar_rect.topleft):
                self.key_choosing(key, key.string, bar)
            distance += 30

        if self.text_keys[0].rect.y + (self.game.keys["MOUSEWHEEL"] * 10) <= 0 \
                and self.text_keys[-1].rect.bottomleft[1] + 10 + (self.game.keys["MOUSEWHEEL"] * 10) >= bar_rect.height:
            self.scroll_y += self.game.keys["MOUSEWHEEL"] * 10

        self.game.screen.blit(bar, bar_rect)
        if self.game.keys["BACK"] or (self.sets_back_button.draw(self.game.screen, False) and self.game.keys["MOUSE DOWN"]):
            self.sub_state = "SETS"
            self.scroll_y = 0

    def key_choosing(self, key, key_name, surface):
        chosen = False
        curr_key = Text(*key.rect.midright, pg.key.name(settings.KEYS[key_name]), key.scale)
        curr_key.rect.x += curr_key.rect.width / 2 + 15
        curr_key.draw(surface)

        if self.game.keys["MOUSE DOWN"]:
            while not chosen:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.game.running, self.game.playing = False, False
                        pg.quit()
                    if event.type == pg.KEYDOWN:
                        if event.key not in settings.KEYS.values() \
                                or settings.KEYS[key_name] == event.key:
                            settings.KEYS[key_name] = event.key
                            chosen = True

    def display_volume(self):
        self.text_volume.draw(self.game.screen)
        bar = pg.surface.Surface((510, 170))
        bar.fill((162, 48, 42))
        bar_rect = bar.get_rect()
        bar_rect.center = (640, 350)
        level, level_rect = None, None

        pos = pg.mouse.get_pos()[0] - bar_rect.x, pg.mouse.get_pos()[1] - bar_rect.y

        distance = 0
        for text in self.volume_text:
            text.rect.y = self.scroll_y + distance
            text.draw(bar)
            pg.draw.rect(bar, (255, 255, 255), (10, text.rect.bottomleft[1], 400, 20), 2)
            level = pg.surface.Surface((getattr(settings, '_'.join(text.string.lower().split())) * 400, 20))
            level.fill((255, 255, 255))
            level_rect = level.get_rect()
            level_rect.topleft = (10, text.rect.bottomleft[1])
            if pg.mouse.get_pressed()[0] and level_rect.collidepoint(pos) and pos[0] <= 400:
                setattr(settings, '_'.join(text.string.lower().split()), pos[0] / 400)
                self.game.player.set_volume()
            bar.blit(level,  level_rect)
            distance += 70

        if self.volume_text[0].rect.y + (self.game.keys["MOUSEWHEEL"] * 10) <= 0 \
                and level_rect.bottomleft[1] + 10 + (self.game.keys["MOUSEWHEEL"] * 10) >= bar_rect.height:
            self.scroll_y += self.game.keys["MOUSEWHEEL"] * 10

        self.game.screen.blit(bar, bar_rect)
        if self.game.keys["BACK"] or (self.sets_back_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]):
            self.sub_state = "SETS"
            self.scroll_y = 0


class GarageMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

        button_sound = pg.mixer.Sound("audio/button_sound.mp3")
        self.garage_close_button = Button(50, 50, "images/buttons/close_button_off.png", "images/buttons/close_button_on.png", button_sound, 0.15)

        self.garage_back_button = Button(290, 360, "images/buttons/back_button_off.png", "images/buttons/back_button_on.png", button_sound, 0.15)
        self.garage_forward_button = Button(990, 360, "images/buttons/forward_button_off.png", "images/buttons/forward_button_on.png", button_sound, 0.15)

    def display_menu(self):
        path = f'images/backgrounds/bgs/{settings.bg["garage_bg"]}/'
        garage_bg = GIF(path)
        garage_bg.resize(1280, 720)
        garage_bg_speed = settings.bg_speed[settings.bg["garage_bg"]]

        cars = []
        for car in settings.cars:
            cars.append((car["specs"], car["name"], Picture(640, 550, f'images/cars/{car["name"]}.png', car["size"])))

        curr_lvl_x = 640
        while self.game.menu_state == "GARAGE" and self.game.running:
            self.check_events()

            garage_bg.draw(self.game.screen, garage_bg_speed)

            # text_curr_car = Text(640, 100, f'Your car: {settings.car}', 20)
            # text_curr_car.draw(self.game.screen)

            distance = 0
            for car in cars:
                center = (curr_lvl_x + distance, 550)
                car[2].rect.center = center
                car[2].draw(self.game.screen)
                if center[0] == 640:
                    self.show_specs(self.game.screen, 100, 200, car[1], car[0])
                distance += 700
            distance -= 700

            if curr_lvl_x + 700 <= 640:
                if (self.garage_back_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]) or (self.game.keys["MOVE LEFT"]):
                    curr_lvl_x += 700

            if curr_lvl_x + distance - 700 >= 640:
                if (self.garage_forward_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]) or (self.game.keys["MOVE RIGHT"]):
                    curr_lvl_x -= 700

            if self.garage_close_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
                self.game.menu_state = "MENU"

            self.game.blit_screen()

        pg.time.delay(500)

    def show_specs(self, surface, x, y, name, specs):
        bar = pg.surface.Surface((470, 220), pg.SRCALPHA)
        bar = bar.convert_alpha()
        bar.fill((0, 0, 0, 200))

        car_name = Text(10, 10, name, 35, set_topleft=True)
        car_name.draw(bar)

        spec_y = 30
        for spec in specs.keys():
            c_1 = Text(10, 10 + spec_y, spec + " " + str(specs[spec]), 30, set_topleft=True, color=BLUE)
            c_1.draw(bar)
            spec_y += 30

        surface.blit(bar, (x, y))


class MusicMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

        button_sound = pg.mixer.Sound("audio/button_sound.mp3")
        self.music_bg = Picture(640, 360, "images/backgrounds/window.png", 0.6)

        self.music_close_button = Button(915, 190, "images/buttons/close_button_off.png", "images/buttons/close_button_on.png", button_sound, 0.2)
        self.random_button_off = Button(450, 485, "images/buttons/random_button_off.png", "images/buttons/random_button_on.png", button_sound, 0.15)
        self.random_button_on = Button(450, 485, "images/buttons/random_button_off1.png", "images/buttons/random_button_on1.png", button_sound, 0.15)
        self.prev_button = Button(540, 485, "images/buttons/prev_button_off.png", "images/buttons/prev_button_on.png", button_sound, 0.2)
        self.play_button = Button(640, 485, "images/buttons/play_button_off.png", "images/buttons/play_button_on.png", button_sound, 0.2)
        self.pause_button = Button(640, 485, "images/buttons/pause_button_off1.png", "images/buttons/pause_button_on1.png", button_sound, 0.2)
        self.next_button = Button(740, 485, "images/buttons/next_button_off.png", "images/buttons/next_button_on.png", button_sound, 0.2)
        self.loop_button_off = Button(830, 485, "images/buttons/loop_button_off.png", "images/buttons/loop_button_on.png", button_sound, 0.15)
        self.loop_button_on = Button(830, 485, "images/buttons/loop_button_off1.png", "images/buttons/loop_button_on1.png", button_sound, 0.15)
        self.song_button = Button(915, 270, "images/buttons/song_button_off.png", "images/buttons/song_button_on.png", button_sound, 0.2)
        self.folder_button = Button(915, 420, "images/buttons/folder_button_off.png", "images/buttons/folder_button_on.png", button_sound, 0.15)
        self.refresh_button = Button(915, 350, "images/buttons/refresh_button_off.png", "images/buttons/refresh_button_on.png", button_sound, 0.2)

        self.plus_button = Button(0, 0, "images/buttons/plus_button_off.png", "images/buttons/plus_button_on.png", None, 0.08)
        self.minus_button = Button(0, 0, "images/buttons/minus_button_off.png", "images/buttons/minus_button_on.png", None, 0.08)
        self.pause_mini_button = Button(0, 0, "images/buttons/pause_button_off.png", "images/buttons/pause_button_on.png", None, 0.08)
        self.play_mini_button = Button(0, 0, "images/buttons/play_button_off.png", "images/buttons/play_button_on.png", None, 0.08)

        self.text_music = Text(640, 195, "MUSIC", 50)
        self.text_playlist = Text(640, 195, "PLAYLIST", 30, None, BLUE)
        self.text_playlist.rect.topleft = (10, 0)
        self.text_others = Text(640, 195, "OTHERS", 30, None, BLUE)

    def display_menu(self):
        self.game.screen.blit(self.music_bg.image, self.music_bg.rect)

        self.text_music.draw(self.game.screen)

        if self.game.player.random_play:
            if self.random_button_on.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
                self.game.player.random_play = False
        else:
            if self.random_button_off.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
                self.game.player.random_play = True

        if self.prev_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
            self.game.player.prev()

        if pg.mixer.music.get_busy():
            if self.pause_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
                self.game.player.pause()
        else:
            if self.play_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
                self.game.player.play()

        if self.game.player.loop:
            if self.loop_button_on.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
                self.game.player.loop = False
        else:
            if self.loop_button_off.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
                self.game.player.loop = True

        if self.next_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
            self.game.player.next()

        if self.song_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
            self.game.player.choose_song()

        if self.folder_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
            self.game.player.choose_dir()
        if self.refresh_button.draw(self.game.screen) and self.game.keys["MOUSE DOWN"]:
            self.game.player.refresh()
            self.text_playlist.rect.topleft = (10, 0)

        self.playlist(self.game.screen)

        if self.music_close_button.draw(self.game.screen, False) and self.game.keys["MOUSE DOWN"]:
            self.game.player.save_to_settings()
            self.game.menu_state = "MENU"

    def playlist(self, surface):
        bar = pg.surface.Surface((538, 220))
        bar.fill((162, 48, 42))
        bar_rect = bar.get_rect()
        bar_rect.center = (604, 330)

        self.text_playlist.draw(bar)
        self.text_others.draw(bar)

        songs = self.game.player.get_songs()
        distance = 10
        for song in songs:
            song[1].rect.topleft = (self.text_playlist.rect.x + 32, self.text_playlist.rect.bottomleft[1] + distance)
            if songs.index(song) == settings.song_number and pg.mixer.music.get_busy():
                self.pause_mini_button.rect.midright = (song[1].rect.midleft[0] - 7, song[1].rect.midleft[1])
                if self.pause_mini_button.draw(bar, surface_topleft=bar_rect.topleft) and self.game.keys["MOUSE DOWN"]:
                    self.game.player.pause()
                song[1].draw_color(bar, mp3_cut=True)
            else:
                self.play_mini_button.rect.midright = (song[1].rect.midleft[0] - 7, song[1].rect.midleft[1])
                if self.play_mini_button.draw(bar, surface_topleft=bar_rect.topleft) and self.game.keys["MOUSE DOWN"]:
                    settings.song_number = songs.index(song)
                    self.game.player.playing = False
                    self.game.player.play()
                song[1].draw(bar, mp3_cut=True)
            pg.draw.rect(bar, (162, 48, 42), (bar_rect.width - 45, song[1].rect.y, 40, 40))
            self.minus_button.rect.midright = (bar_rect.width - 7, song[1].rect.midleft[1])
            if self.minus_button.draw(bar, surface_topleft=bar_rect.topleft) and self.game.keys["MOUSE DOWN"]:
                self.game.player.pop_from_playlist(song)
            distance += 30

        self.text_others.rect.topleft = (self.text_playlist.rect.x, self.text_playlist.rect.bottomleft[1] + 10 + distance)
        distance += 50
        others = self.game.player.get_others()
        for song in others:
            song[1].rect.topleft = (self.text_playlist.rect.x + 32, self.text_playlist.rect.bottomleft[1] + distance)
            if others.index(song) + len(songs) == settings.song_number and pg.mixer.music.get_busy():
                self.pause_mini_button.rect.midright = (song[1].rect.midleft[0] - 7, song[1].rect.midleft[1])
                if self.pause_mini_button.draw(bar, surface_topleft=bar_rect.topleft) and self.game.keys["MOUSE DOWN"]:
                    self.game.player.pause()
                song[1].draw_color(bar, mp3_cut=True)
            else:
                self.play_mini_button.rect.midright = (song[1].rect.midleft[0] - 7, song[1].rect.midleft[1])
                if self.play_mini_button.draw(bar, surface_topleft=bar_rect.topleft) and self.game.keys["MOUSE DOWN"]:
                    settings.song_number = others.index(song) + len(songs)
                    self.game.player.playing = False
                    self.game.player.play()
                song[1].draw(bar, mp3_cut=True)
            pg.draw.rect(bar, (162, 48, 42), (bar_rect.width - 45, song[1].rect.y, 40, 40))
            self.plus_button.rect.midright = (bar_rect.width - 7, song[1].rect.midleft[1])
            if self.plus_button.draw(bar, surface_topleft=bar_rect.topleft) and self.game.keys["MOUSE DOWN"]:
                self.game.player.pop_from_others(song)
            distance += 30

        l_1 = self.text_others.rect.bottomleft[1]
        if others:
            l_1 = others[-1][1].rect.bottomleft[1]

        if self.text_playlist.rect.y + (self.game.keys["MOUSEWHEEL"] * 10) <= 4 \
                and l_1 + 5 + (self.game.keys["MOUSEWHEEL"] * 10) >= bar_rect.height - 7:
            self.text_playlist.rect.y += self.game.keys["MOUSEWHEEL"] * 10

        surface.blit(bar, bar_rect)
        pg.draw.rect(self.game.screen, 'white', (bar_rect.x, bar_rect.y, 538, 220), 1)
