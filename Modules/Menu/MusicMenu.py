from .Menu import *


class MusicMenu(Menu):

    def __init__(self, game):
        super().__init__(game)

        button_sound = pg.mixer.Sound("Resources/Audio/button_sound.mp3")
        self._music_bg = Picture("Resources/Images/Backgrounds/window.png", 0.6)

        self._music_close_button = Button("Resources/Images/Buttons/close_button_off.png",
                                          "Resources/Images/Buttons/close_button_on.png", button_sound, 0.15)
        self._random_button_off = Button("Resources/Images/Buttons/random_button_off.png",
                                         "Resources/Images/Buttons/random_button_on.png", button_sound, 0.15)
        self._random_button_on = Button("Resources/Images/Buttons/random_button_off1.png",
                                        "Resources/Images/Buttons/random_button_on1.png", button_sound, 0.15)
        self._prev_button = Button("Resources/Images/Buttons/prev_button_off.png",
                                   "Resources/Images/Buttons/prev_button_on.png",
                                   button_sound, 0.2)
        self._play_button = Button("Resources/Images/Buttons/play_button_off.png",
                                   "Resources/Images/Buttons/play_button_on.png",
                                   button_sound, 0.2)
        self._pause_button = Button("Resources/Images/Buttons/pause_button_off1.png",
                                    "Resources/Images/Buttons/pause_button_on1.png", button_sound, 0.2)
        self._next_button = Button("Resources/Images/Buttons/next_button_off.png",
                                   "Resources/Images/Buttons/next_button_on.png",
                                   button_sound, 0.2)
        self._loop_button_off = Button("Resources/Images/Buttons/loop_button_off.png",
                                       "Resources/Images/Buttons/loop_button_on.png", button_sound, 0.15)
        self._loop_button_on = Button("Resources/Images/Buttons/loop_button_off1.png",
                                      "Resources/Images/Buttons/loop_button_on1.png", button_sound, 0.15)
        self._song_button = Button("Resources/Images/Buttons/song_button_off.png",
                                   "Resources/Images/Buttons/song_button_on.png",
                                   button_sound, 0.15)
        self._folder_button = Button("Resources/Images/Buttons/folder_button_off.png",
                                     "Resources/Images/Buttons/folder_button_on.png", button_sound, 0.15)
        self._refresh_button = Button("Resources/Images/Buttons/refresh_button_off.png",
                                      "Resources/Images/Buttons/refresh_button_on.png", button_sound, 0.16)

        self._plus_button = Button("Resources/Images/Buttons/plus_button_off.png",
                                   "Resources/Images/Buttons/plus_button_on.png", None,
                                   0.08)
        self._minus_button = Button("Resources/Images/Buttons/minus_button_off.png",
                                    "Resources/Images/Buttons/minus_button_on.png",
                                    None, 0.08)
        self._pause_mini_button = Button("Resources/Images/Buttons/pause_button_off.png",
                                         "Resources/Images/Buttons/pause_button_on.png", None, 0.08)
        self._play_mini_button = Button("Resources/Images/Buttons/play_button_off.png",
                                        "Resources/Images/Buttons/play_button_on.png",
                                        None, 0.08)

        self._text_music = Text("MUSIC", 50)
        self._text_playlist = Text("PLAYLIST", 30, None, color=BLUE)
        self._text_playlist.rect.topleft = (10, 0)
        self._text_others = Text("OTHERS", 30, None, color=BLUE)  # 640, 195,

        self._scroll_y = 0

    def display_menu(self):
        self._music_bg.draw(self.game.screen, (640, 360))

        self._text_music.draw(self.game.screen, (640, 190))

        if self.game.music_player.random_play:
            if self._random_button_on.draw(self.game.screen, (450, 485)) and self.game.keys["MOUSE DOWN"]:
                self.game.music_player.random_play = False
        else:
            if self._random_button_off.draw(self.game.screen, (450, 485)) and self.game.keys["MOUSE DOWN"]:
                self.game.music_player.random_play = True

        if self._prev_button.draw(self.game.screen, (540, 483)) and self.game.keys["MOUSE DOWN"]:
            self.game.music_player.prev()

        if pg.mixer.music.get_busy():
            if self._pause_button.draw(self.game.screen, (640, 483)) and self.game.keys["MOUSE DOWN"]:
                self.game.music_player.pause()
        else:
            if self._play_button.draw(self.game.screen, (640, 483)) and self.game.keys["MOUSE DOWN"]:
                self.game.music_player.play()

        if self.game.music_player.loop:
            if self._loop_button_on.draw(self.game.screen, (830, 485)) and self.game.keys["MOUSE DOWN"]:
                self.game.music_player.loop = False
        else:
            if self._loop_button_off.draw(self.game.screen, (830, 485)) and self.game.keys["MOUSE DOWN"]:
                self.game.music_player.loop = True

        if self._next_button.draw(self.game.screen, (740, 483)) and self.game.keys["MOUSE DOWN"]:
            self.game.music_player.next()

        if self._song_button.draw(self.game.screen, (915, 260)) and self.game.keys["MOUSE DOWN"]:
            self.game.music_player.choose_song()

        if self._folder_button.draw(self.game.screen, (915, 400)) and self.game.keys["MOUSE DOWN"]:
            self.game.music_player.choose_dir()
            self._scroll_y = 0

        if self._refresh_button.draw(self.game.screen, (915, 330)) and self.game.keys["MOUSE DOWN"]:
            self.game.music_player.refresh()
            self._scroll_y = 0

        self.__display_playlist(self.game.screen)

        if self._music_close_button.draw(self.game.screen, (915, 190)) and self.game.keys["MOUSE DOWN"]:
            self.game.music_player.save_to_settings()
            self.game.menu_state = "MENU"

    def __display_playlist(self, surface):
        bar = pg.surface.Surface((538, 220)).convert_alpha()
        bar.fill(BROWN)
        bar_rect = bar.get_rect()
        bar_rect.center = (604, 328)

        self._text_playlist.draw(bar, (10, self._scroll_y), position="topleft")

        songs = self.game.music_player.get_songs()
        distance = 10
        for song in songs:
            if self.game.music_player.song_number == songs.index(song):
                if pg.mixer.music.get_busy():
                    song[1].draw(bar,
                                 (self._text_playlist.rect.x + 32, self._text_playlist.rect.bottomleft[1] + distance),
                                 position="topleft", mp3_cut=True, color=YELLOW)
                    if self._pause_mini_button.draw(bar, (song[1].rect.midleft[0] - 7, song[1].rect.midleft[1]),
                                                    position="midright", surface_topleft=bar_rect.topleft) and \
                            self.game.keys["MOUSE DOWN"]:
                        self.game.music_player.pause()
                else:
                    song[1].draw(bar,
                                 (self._text_playlist.rect.x + 32, self._text_playlist.rect.bottomleft[1] + distance),
                                 position="topleft", mp3_cut=True)
                    if self._play_mini_button.draw(bar, (song[1].rect.midleft[0] - 7, song[1].rect.midleft[1]),
                                                   position="midright", surface_topleft=bar_rect.topleft) and \
                            self.game.keys["MOUSE DOWN"]:
                        self.game.music_player.play()
            else:
                song[1].draw(bar, (self._text_playlist.rect.x + 32, self._text_playlist.rect.bottomleft[1] + distance),
                             position="topleft", mp3_cut=True)
                if self._play_mini_button.draw(bar, (song[1].rect.midleft[0] - 7, song[1].rect.midleft[1]),
                                               position="midright", surface_topleft=bar_rect.topleft) and \
                        self.game.keys[
                            "MOUSE DOWN"]:
                    self.game.music_player.song_number = songs.index(song)
                    self.game.music_player.playing = False
                    self.game.music_player.paused = False
                    self.game.music_player.play()
            pg.draw.rect(bar, BROWN, (bar_rect.width - 40, song[1].rect.y, 40, 40))
            if self._minus_button.draw(bar, (bar_rect.width - 7, song[1].rect.midleft[1]), position="midright",
                                       surface_topleft=bar_rect.topleft) and self.game.keys["MOUSE DOWN"]:
                self.game.music_player.pop_from_playlist(song)
            distance += 30

        self._text_others.draw(bar,
                               (self._text_playlist.rect.x, self._text_playlist.rect.bottomleft[1] + 10 + distance),
                               position="topleft")
        distance += 50
        others = self.game.music_player.get_others()
        for song in others:
            if self.game.music_player.song_number == others.index(song) + len(songs):
                if pg.mixer.music.get_busy():
                    song[1].draw(bar,
                                 (self._text_playlist.rect.x + 32, self._text_playlist.rect.bottomleft[1] + distance),
                                 position="topleft", mp3_cut=True, color=YELLOW)
                    if self._pause_mini_button.draw(bar, (song[1].rect.midleft[0] - 7, song[1].rect.midleft[1]),
                                                    position="midright", surface_topleft=bar_rect.topleft) and \
                            self.game.keys["MOUSE DOWN"]:
                        self.game.music_player.pause()
                else:
                    song[1].draw(bar,
                                 (self._text_playlist.rect.x + 32, self._text_playlist.rect.bottomleft[1] + distance),
                                 position="topleft", mp3_cut=True)
                    if self._play_mini_button.draw(bar, (song[1].rect.midleft[0] - 7, song[1].rect.midleft[1]),
                                                   position="midright", surface_topleft=bar_rect.topleft) and \
                            self.game.keys["MOUSE DOWN"]:
                        self.game.music_player.play()
            else:
                song[1].draw(bar, (self._text_playlist.rect.x + 32, self._text_playlist.rect.bottomleft[1] + distance),
                             position="topleft", mp3_cut=True)
                if self._play_mini_button.draw(bar, (song[1].rect.midleft[0] - 7, song[1].rect.midleft[1]),
                                               position="midright", surface_topleft=bar_rect.topleft) and \
                        self.game.keys[
                            "MOUSE DOWN"]:
                    self.game.music_player.song_number = others.index(song) + len(songs)
                    self.game.music_player.playing = False
                    self.game.music_player.paused = False
                    self.game.music_player.play()
            pg.draw.rect(bar, BROWN, (bar_rect.width - 40, song[1].rect.y, 40, 40))
            if self._plus_button.draw(bar, (bar_rect.width - 7, song[1].rect.midleft[1]), position="midright",
                                      surface_topleft=bar_rect.topleft) and self.game.keys["MOUSE DOWN"]:
                self.game.music_player.pop_from_others(song)
            distance += 30

        l_1 = self._text_others.rect.bottomleft[1]
        if others:
            l_1 = others[-1][1].rect.bottomleft[1]

        if self._text_playlist.rect.y + (self.game.keys["MOUSEWHEEL"] * 10) <= 4 \
                and l_1 + 5 + (self.game.keys["MOUSEWHEEL"] * 10) >= bar_rect.height - 7:
            self._scroll_y += self.game.keys["MOUSEWHEEL"] * 10

        surface.blit(bar, bar_rect)
        pg.draw.rect(self.game.screen, 'white', (bar_rect.x, bar_rect.y, 538, 220), 1)  # WHITE BORDER
