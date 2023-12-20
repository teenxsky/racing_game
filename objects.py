import pygame
import pygame as pg
from settings import *
import random
import os
from tkinter import Tk
from tkinter import filedialog

root = Tk()
root.withdraw()


class Button:
    def __init__(self, x, y, image_off_name, image_on_name, sound=None, scale=1):
        self.image_off = pg.image.load(image_off_name).convert_alpha()
        self.image_on = pg.image.load(image_on_name).convert_alpha()

        self.click_sound = sound

        # FOR NON-PUSHED BUTTON

        width_off = self.image_off.get_width()
        height_off = self.image_off.get_height()
        self.image_off = pg.transform.scale(self.image_off, (int(width_off * scale), int(height_off * scale)))
        self.rect = self.image_off.get_rect()
        self.rect.center = (x, y)

        # FOR PUSHED BUTTON

        width_on = self.image_on.get_width()
        height_on = self.image_on.get_height()
        self.image_on = pg.transform.scale(self.image_on, (int(width_on * scale), int(height_on * scale)))

        # FOR BUTTON PUSHING

        self.on_button = False

    def draw(self, surface, block=False, surface_topleft=(0, 0)):
        action = False
        x, y = surface_topleft
        if not block:
            pos = pg.mouse.get_pos()
            x_b = (pos[0] >= x) and (pos[0] <= x + surface.get_width())
            y_b = (pos[1] >= y) and (pos[1] <= y + surface.get_height())
            if self.rect.collidepoint((pos[0] - x, pos[1] - y)) and x_b and y_b:
                if not self.on_button:
                    self.on_button = True
                    if self.click_sound:
                        self.click_sound.play()

                surface.blit(self.image_on, (self.rect.x, self.rect.y))
                action = True
            else:
                self.on_button = False
                surface.blit(self.image_off, (self.rect.x, self.rect.y))

        else:
            surface.blit(self.image_off, (self.rect.x, self.rect.y))

        return action


class Picture:
    def __init__(self, x, y, image_name, scale=1):
        image = pg.image.load(image_name).convert_alpha()
        width = image.get_width()
        height = image.get_height()

        self.image = pg.transform.scale(image, (width * scale, height * scale))
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.center = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.center

        self.current_size = 0
        self.pulse = True

        self.last_update = pg.time.get_ticks()

    def resize(self, width, height):
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def draw(self, surface):
        action = False
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            action = True
        surface.blit(self.image, self.rect)
        return action

    def draw_with_pulse(self, surface, size=20, time=15):  # FOR JUMPING GAME TITLE
        current_time = pg.time.get_ticks()

        if current_time - self.last_update >= time:
            if self.pulse:
                self.current_size += 1
                if self.current_size == size:
                    self.pulse = False
            else:
                self.current_size -= 1
                if self.current_size == 0:
                    self.pulse = True
            self.last_update = current_time

        new = self.width + self.current_size, self.height + self.current_size
        current_image = pg.transform.scale(self.image, new)
        current_rect = current_image.get_rect(center=self.rect.center)
        surface.blit(current_image, current_rect)


class Background(Picture):
    def __init__(self, image_name, scale=1):
        super().__init__(0, 0, image_name, scale)

        self.bg_y = 0

        self.bgs = []
        self.bgs_origin, self.cum_w, self.k = [], 0, 0
        self.scrolls = 0
        self.last_bg = self

    def scroll(self, surface, speed):
        self.bg_y += speed
        surface.blit(self.image, (0, self.bg_y))
        surface.blit(self.image, (0, self.bg_y - 720))
        if self.bg_y == 720:
            self.bg_y = 0

    def set_bgs(self, bgs, cum_weight, k=10):
        self.bgs = random.choices(bgs, cum_weights=cum_weight, k=k)
        self.bgs_origin, self.cum_w, self.k = bgs, cum_weight, k

    def random_scroll(self, surface, speed):
        self.bg_y += speed

        if self.scrolls == 0:
            surface.blit(self.last_bg.image, (0, self.bg_y))
            surface.blit(self.bgs[self.scrolls].image, (0, self.bg_y - 720))
        else:
            surface.blit(self.bgs[self.scrolls - 1].image, (0, self.bg_y))
            surface.blit(self.bgs[self.scrolls].image, (0, self.bg_y - 720))

        if (self.scrolls == len(self.bgs) - 1) and (self.bg_y >= 720):
            self.last_bg = self.bgs[self.scrolls]
            self.set_bgs(self.bgs_origin, self.cum_w, self.k)
            self.scrolls = -1

        if self.bg_y >= 720:
            self.bg_y = 0
            self.scrolls += 1


class HUD:
    def __init__(self, coins_size=1):
        gold_coin_image = pg.image.load("images/HUD/coins/MonedaD.png").convert_alpha()
        self.coins_sheets = self.get_sheets(gold_coin_image)
        self.frame = 0

        self.last_update = pg.time.get_ticks()

    def get_image(self, sheet, frame, scale=1, colour=(0, 0, 0)):
        width, height = sheet.get_height(), sheet.get_height()
        image = pg.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
        image = pg.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image

    def get_sheets(self, image):
        sheets = []
        for i in range(image.get_width() // image.get_height()):
            sheets.append(self.get_image(image, i, 5))
        return sheets

    def draw_coins(self, surface, x, y, time): # Сделать в ХУД класс выведения коин или другого на экран со всеми примочками
        current_time = pg.time.get_ticks()

        coin_rect = self.coins_sheets[0].get_rect()
        coin_rect.center = (x, y)

        coin_val = Text(x + 70, y, str(settings.coins), 50)
        coin_val.rect.midleft = (coin_rect.midright[0] + 5, coin_rect.midright[1])

        surface.blit(self.coins_sheets[self.frame], coin_rect)
        surface.blit(coin_val.text, coin_val.rect)

        if current_time - self.last_update >= time:
            self.frame += 1
            self.last_update = current_time
            if self.frame == len(self.coins_sheets):
                self.frame = 0

class Text:
    def __init__(self, x, y, text='', scale=20, sound=None, color=(255, 255, 255), set_topleft=False):
        self.center = (x, y)
        self.scale = scale
        self.sound = sound
        self.color = color
        self.string = text

        self.font = pg.font.Font("fonts/pxl_tactical.ttf", self.scale)
        self.text = self.font.render(self.string, False, self.color).convert_alpha()
        self.rect = self.text.get_rect()
        if set_topleft:
            self.rect.topleft = (x, y)
        else:
            self.rect.center = (x, y)

        self.on_button = False

    def draw(self, surface, mp3_cut=False):
        if mp3_cut:
            text = self.font.render(self.string[:-4], False, self.color).convert_alpha()
            surface.blit(text, self.rect)
        else:
            surface.blit(self.text, self.rect)

    def draw_color(self, surface, color=(255, 255, 200), mp3_cut=False):
        if mp3_cut:
            text = self.font.render(self.string[:-4], False, color).convert_alpha()
        else:
            text = self.font.render(self.string, False, color).convert_alpha()
        surface.blit(text, self.rect)

    def draw_as_button(self, surface, surface_topleft=(0, 0), press_color=(255, 255, 200)):
        action = False
        x, y = surface_topleft
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint((pos[0] - x, pos[1] - y)):
            action = True
            if not self.on_button:
                self.on_button = True
                if self.sound:
                    self.sound.play()
            press_text = self.font.render(self.string, False, press_color).convert_alpha()
            surface.blit(press_text, self.rect)
        else:
            self.on_button = False
            surface.blit(self.text, self.rect)

        return action

    def typing(self, surface):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DELETE and len(self.string) > 0:
                    self.string = self.string[:-1]
                else:
                    self.string += event.unicode

        self.text = self.font.render(self.string, False, self.color).convert_alpha()
        self.rect = self.text.get_rect()
        self.rect.center = self.center
        self.draw(surface)


class GIF:
    def __init__(self, path, scale=1):
        self.path = path
        self.gif = []

        for file in sorted(os.listdir(self.path)):
            self.gif.append(Picture(640, 360, self.path + file, scale=scale))

        self.last_update = pg.time.get_ticks()
        self.frame = 0

    def resize(self, width, height):
        for frame in self.gif:
            frame.resize(width, height)

    def move(self, x, y):
        for frame in self.gif:
            frame.rect.center = (x, y)

    def draw(self, screen, speed=20):
        current_time = pg.time.get_ticks()
        if current_time - self.last_update >= speed:
            self.last_update = current_time
            self.frame += 1
            if self.frame == len(self.gif):
                self.frame = 0
        self.gif[self.frame].draw(screen)


class MusicPlayer:
    def __init__(self, path):
        self.path = path
        self.playlist = []
        self.others = []
        # self.covers

        self.playing = False
        self.random_play = True
        self.loop = False
        self.MUSIC_END = pg.USEREVENT+1
        pg.mixer.music.set_endevent(self.MUSIC_END)

        self.playlist = list((file_path, Text(400, 270, file, 20)) for file_path, file in settings.songs if os.path.exists(file_path + file))
        self.others = list((file_path, Text(400, 270, file, 20)) for file_path, file in settings.others if os.path.exists(file_path + file))

    def play(self):
        if not self.playing:
            self.playing = True
            if settings.song_number < len(self.playlist):
                path = self.playlist[settings.song_number][0]
                file = self.playlist[settings.song_number][1].string
            else:
                path = self.others[settings.song_number % len(self.playlist)][0]
                file = self.others[settings.song_number % len(self.playlist)][1].string
            try:
                pg.mixer.music.load(path + file)
            except pygame.error:
                self.playlist = list((file_path, Text(400, 270, file, 20)) for file_path, file in settings.songs if os.path.exists(file_path + file))
                self.others = list((file_path, Text(400, 270, file, 20)) for file_path, file in settings.others if os.path.exists(file_path + file))
            pg.mixer.music.play()
        else:
            pg.mixer.music.unpause()

    def pause(self):
        pg.mixer.music.pause()

    def next(self):
        self.playing = False
        if self.random_play:
            settings.song_number = random.randrange(0, len(self.playlist) + len(self.others) - 1)
        else:
            settings.song_number += 1
            if settings.song_number == len(self.playlist) + len(self.others):
                settings.song_number = 0
        self.play()

    def prev(self):
        self.playing = False
        if self.random_play:
            settings.song_number = random.randrange(0, len(self.playlist) + len(self.others) - 1)
        else:
            settings.song_number -= 1
            if settings.song_number < 0:
                settings.song_number = len(self.playlist) + len(self.others) - 1
        self.play()

    def get_songs(self):
        return self.playlist

    def get_others(self):
        return self.others

    def set_volume(self):
        pg.mixer.music.set_volume(settings.music_volume)

    def choose_dir(self):
        self.path = filedialog.askdirectory(title="Choosing directory", initialdir="Desktop") + "/"
        self.refresh()

    def choose_song(self):
        file = filedialog.askopenfilename(title="Choosing directory")
        if file:
            path, name = "/".join(file.split("/")[:-1]) + "/", file.split("/")[-1]
            self.others.append((path, Text(400, 270, name, 20)))

    def pop_from_playlist(self, song):
        if self.playlist.index(song) == settings.song_number:
            self.playlist.remove(song)
            self.others.append(song)
            settings.song_number = self.others.index(song) + len(self.playlist)
        else:
            self.playlist.remove(song)
            self.others.append(song)

    def pop_from_others(self, song):
        if self.others.index(song) + len(self.playlist) == settings.song_number:
            self.others.remove(song)
            self.playlist.append(song)
            settings.song_number = self.playlist.index(song)
        else:
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
        self.playlist = list((self.path, Text(400, 270, file, 20)) for file in sorted(os.listdir(self.path)) if ".mp3" in file)
        settings.song_number = 0
        self.others = []
        self.save_to_settings()
