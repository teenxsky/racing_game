import pygame as pg
import os
import random
import eyed3
from tkinter import filedialog
from tkinter import Tk
from Modules.Objects.GUIObjects.Picture import Picture
from Modules.Objects.GUIObjects.Text import Text
from Modules.Objects.GUIObjects.Button import Button
from .Settings import settings, config


root = Tk()
root.withdraw()


class MusicPlayer:
    def __init__(self):
        self.MUSIC_DIR_PATH = config.MUSIC_DIR_PATH
        self.COVERS_PATH = config.COVERS_PATH
        self.SONGS = settings.songs
        self.OTHERS = settings.others

        self.playlist = []
        self.playlist = list((file_path, Text(file, 20)) for file_path, file in self.SONGS if
                             os.path.exists(file_path + file))
        self.others = []
        self.others = list((file_path, Text(file, 20)) for file_path, file in self.OTHERS if
                           os.path.exists(file_path + file))

        self.song_number = 0

        self.covers = []
        self.__load_covers()
        if self.playlist or self.others:
            self.__set_current_cover()

        self.playing = False
        self.paused = False
        self.random_play = False
        self.loop = False
        self.current_cover = None
        self.MUSIC_END = pg.USEREVENT + 1
        pg.mixer.music.set_endevent(self.MUSIC_END)

        self.running_string_x = 0
        self.running_update = pg.time.get_ticks()

        # FOR DRAWING SONG

        button_sound = pg.mixer.Sound("Resources/Audio/button_sound.mp3")
        self._prev_button = Button("Resources/Images/Buttons/prev_button_off.png",
                                   "Resources/Images/Buttons/prev_button_on.png",
                                   button_sound, 0.11)
        self._play_button = Button("Resources/Images/Buttons/play_button_off.png",
                                   "Resources/Images/Buttons/play_button_on.png",
                                   button_sound, 0.11)
        self._pause_button = Button("Resources/Images/Buttons/pause_button_off1.png",
                                    "Resources/Images/Buttons/pause_button_on1.png", button_sound, 0.11)
        self._next_button = Button("Resources/Images/Buttons/next_button_off.png",
                                   "Resources/Images/Buttons/next_button_on.png",
                                   button_sound, 0.11)
        self.bar_width = self._prev_button.rect.width + self._play_button.rect.width + self._next_button.rect.width + 20
        self.bar_height = max(self._prev_button.rect.height, self._play_button.rect.height, self._next_button.rect.height)

    def play(self):
        if not self.playing and not self.paused and (self.playlist or self.others):
            self.playing = True
            if self.song_number < len(self.playlist):
                path = self.playlist[self.song_number][0]
                file = self.playlist[self.song_number][1].string
            else:
                path = self.others[self.song_number - len(self.playlist)][0]
                file = self.others[self.song_number - len(self.playlist)][1].string
            try:
                pg.mixer.music.load(path + file)
            except pg.error:
                self.playlist = list((file_path, Text(file, 20)) for file_path, file in settings.songs if
                                     os.path.exists(file_path + file))
                self.others = list((file_path, Text(file, 20)) for file_path, file in settings.others if
                                   os.path.exists(file_path + file))
            pg.mixer.music.play(fade_ms=200)
            self.__set_current_cover()
            self.running_string_x = 0
        elif self.playlist or self.others:
            if self.paused:
                self.unpause()
            else:
                self.pause()

    def next(self):
        self.playing = False
        self.paused = False
        if self.random_play:
            self.song_number = random.randrange(0, len(self.playlist) - 1)
        else:
            self.song_number += 1
            if self.song_number == len(self.playlist) + len(self.others) or self.song_number >= len(
                    self.playlist):
                self.song_number = 0
        self.play()

    def prev(self):
        self.playing = False
        self.paused = False
        if self.random_play:
            self.song_number = random.randrange(0, len(self.playlist) - 1)
        else:
            self.song_number -= 1
            if self.song_number < 0:
                self.song_number = len(self.playlist) + len(self.others) - 1
            elif self.song_number >= len(self.playlist):
                self.song_number = 0
        self.play()

    def get_songs(self):
        return self.playlist

    def get_others(self):
        return self.others

    def unpause(self):
        pg.mixer.music.unpause()
        self.paused = False

    def pause(self):
        pg.mixer.music.pause()
        self.paused = True

    @staticmethod
    def set_volume():
        pg.mixer.music.set_volume(settings.music_volume)

    def choose_dir(self):
        path = filedialog.askdirectory(title="Choosing directory", initialdir="Desktop")
        if path:
            self.MUSIC_DIR_PATH = path + '/'
            self.refresh()

    def choose_song(self):
        file = filedialog.askopenfilename(title="Choosing directory")
        if file:
            path, name = "/".join(file.split("/")[:-1]) + "/", file.split("/")[-1]
            if (path, Text(name, 20)) not in self.playlist + self.others:
                self.others.append((path, Text(name, 20)))

    def pop_from_playlist(self, song):
        if self.playlist.index(song) == self.song_number:
            self.song_number = len(self.others) + len(self.playlist) - 1
        elif self.playlist.index(song) < self.song_number:
            self.song_number -= 1
        self.playlist.remove(song)
        self.others.append(song)

    def pop_from_others(self, song):
        if self.others.index(song) + len(self.playlist) == self.song_number:
            self.song_number = len(self.playlist)
        elif self.others.index(song) + len(self.playlist) > self.song_number:
            self.song_number += 1 * (len(self.playlist) <= self.song_number)
        self.others.remove(song)
        self.playlist.append(song)

    def save_to_settings(self):
        curr_songs = []
        for path, file in self.playlist:
            curr_songs.append((path, file.string))
        settings.songs = curr_songs

        curr_songs = []
        for path, file in self.others:
            curr_songs.append((path, file.string))
        settings.others = curr_songs

    def refresh(self):
        self.playlist = list(
            (self.MUSIC_DIR_PATH, Text(file, 20)) for file in sorted(os.listdir(self.MUSIC_DIR_PATH)) if file.endswith(".mp3"))
        self.MUSIC_DIR_PATH = config.MUSIC_DIR_PATH
        self.others = []
        self.save_to_settings()
        self.clean_covers()
        self.__load_covers()
        self.__set_current_cover()
        pg.mixer.music.stop()
        self.playing = False
        self.song_number = 0
        if os.listdir(self.MUSIC_DIR_PATH):
            self.play()

    def __set_current_cover(self):
        tracks = self.playlist + self.others
        song_name = tracks[self.song_number][1].string[:-4]
        for cover in self.covers:
            if song_name in cover[0].string:
                cover_img = Picture(cover[1], (80, 80))
                self.current_cover = (song_name, cover_img)
                break

    def clean_covers(self):
        for cover in sorted(os.listdir(self.COVERS_PATH)):
            if cover[-4:] == ".png" and cover != "default.png":
                os.remove(self.COVERS_PATH + cover)

    def __load_covers(self):
        for path, song in self.playlist + self.others:
            audiofile = eyed3.load(path + song.string)
            for image in audiofile.tag.images:
                if image:
                    with open(self.COVERS_PATH + song.string[:-4] + '.png', 'wb+') as f:
                        f.write(image.image_data)
                    self.covers.append((song, self.COVERS_PATH + song.string[:-4] + '.png'))
            self.covers.append((song, self.COVERS_PATH + 'default.png'))

    def draw_current_song(self, surface, coordinates, scale=0.5, position="center", text_up=False, game=None, block=False):
        """argument 'game' 'block' are for drawing the player interface(e.g. 'play button'), the 'game' arg is supposed to be an instance of the main class Game"""
        if self.playlist or self.others:
            song_name, cover = self.current_cover

            setattr(cover.rect, position, coordinates)

            song_names = [Text(song_name, int(scale * 40)),
                          Text(song_name, int(scale * 40)),
                          Text(song_name, int(scale * 40))]

            text_bar = pg.Surface((200, song_names[0].rect.height), pg.SRCALPHA).convert_alpha()
            text_bar.fill((0, 0, 0, 0))
            text_bar_rect = text_bar.get_rect()

            if position.endswith("left"):
                if text_up:
                    text_bar_rect.topleft = cover.rect.topright[0] + 10, cover.rect.topright[1]
                else:
                    text_bar_rect.bottomleft = cover.rect.bottomright[0] + 10, cover.rect.bottomright[1]
            elif position.endswith("right"):
                if text_up:
                    text_bar_rect.topright = cover.rect.topleft[0] - 10, cover.rect.topleft[1]
                else:
                    text_bar_rect.bottomright = cover.rect.bottomleft[0] - 10, cover.rect.bottomleft[1]
            else:
                if text_up:
                    text_bar_rect.midbottom = cover.rect.midtop[0], cover.rect.midtop[1] - 10
                else:
                    text_bar_rect.midtop = cover.rect.midbottom[0], cover.rect.midbottom[1] + 10

            if pg.time.get_ticks() - self.running_update >= 100 and not self.paused:
                self.running_string_x += 5
                self.running_update = pg.time.get_ticks()

            i = None
            for i in range(len(song_names)):
                if not i:
                    song_names[i].draw(text_bar, (self.running_string_x, text_bar_rect.height // 2), position="midright")
                else:
                    song_names[i].draw(text_bar, (song_names[i-1].rect.midleft[0] - 10, text_bar_rect.height // 2), position="midright")

            if song_names[i].rect.midleft[0] >= text_bar_rect.width:
                self.running_string_x = 0

            cover.draw(surface, coordinates, position=position)
            surface.blit(text_bar, text_bar_rect)

            if game:
                controls_bar = pg.Surface((self.bar_width, self.bar_height), pg.SRCALPHA).convert_alpha()
                controls_bar.fill((0, 0, 0, 0))
                controls_bar_rect = controls_bar.get_rect()

                if position.endswith("left"):
                    if text_up:
                        controls_bar_rect.topleft = text_bar_rect.bottomleft[0], text_bar_rect.bottomleft[1] + 10
                    else:
                        controls_bar_rect.bottomleft = text_bar_rect.topleft[0], text_bar_rect.topleft[1] - 10
                elif position.endswith("right"):
                    if text_up:
                        controls_bar_rect.topright = text_bar_rect.bottomright[0], text_bar_rect.bottomright[1] + 10
                    else:
                        controls_bar_rect.bottomright = text_bar_rect.topright[0], text_bar_rect.topright[1] - 10
                else:
                    controls_bar_rect.center = cover.rect.center

                if pg.mixer.music.get_busy():
                    if self._pause_button.draw(controls_bar, (controls_bar_rect.width // 2, controls_bar_rect.height // 2), surface_topleft=controls_bar_rect.topleft, position="center", block=block) and game.keys["MOUSE DOWN"]:
                        game.music_player.pause()
                else:
                    if self._play_button.draw(controls_bar, (controls_bar_rect.width // 2, controls_bar_rect.height // 2), surface_topleft=controls_bar_rect.topleft, position="center", block=block) and game.keys["MOUSE DOWN"]:
                        game.music_player.play()

                if self._next_button.draw(controls_bar, (controls_bar_rect.width, controls_bar_rect.height // 2), surface_topleft=controls_bar_rect.topleft, position="midright", block=block) and game.keys["MOUSE DOWN"]:
                    game.music_player.next()
                if self._prev_button.draw(controls_bar, (0, controls_bar_rect.height // 2), surface_topleft=controls_bar_rect.topleft, position="midleft", block=block) and game.keys["MOUSE DOWN"]:
                    game.music_player.prev()

                surface.blit(controls_bar, controls_bar_rect)
