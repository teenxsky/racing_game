import pygame
import pygame as pg
from settings import *
import random
import os
from tkinter import Tk
from tkinter import filedialog
import eyed3
import eyed3.id3
import eyed3.id3.frames

root = Tk()
root.withdraw()


# FUNCTIONS

def get_sheets(image, frames, scale=1):
    width, height = image.get_width(), image.get_height()
    sheets = []
    for frame in range(frames):
        image_area = pg.Surface(((width // frames), height)).convert_alpha()
        image_area.blit(image, (0, 0), ((frame * (width // frames)), 0, (width // frames), height))
        image_area = pg.transform.scale(image_area, ((width // frames) * scale, height * scale))
        image_area.set_colorkey((0, 0, 0))
        sheets.append(image_area)
    return sheets


class Button:
    def __init__(self, x, y, image_off_name, image_on_name, sound=None, scale=1, set_topleft=False, set_midleft=False,
                 set_midright=False, set_midbottom=False):
        self.image_off = pg.image.load(image_off_name).convert_alpha()
        self.image_on = pg.image.load(image_on_name).convert_alpha()

        self.click_sound = sound

        # FOR NON-PUSHED BUTTON

        width_off = self.image_off.get_width()
        height_off = self.image_off.get_height()
        self.image_off = pg.transform.scale(self.image_off, (int(width_off * scale), int(height_off * scale)))
        self.rect = self.image_off.get_rect()

        if set_topleft:
            self.rect.topleft = (x, y)
        elif set_midleft:
            self.rect.midleft = (x, y)
        elif set_midright:
            self.rect.midright = (x, y)
        elif set_midbottom:
            self.rect.midbottom = (x, y)
        else:
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
    def __init__(self, x, y, image_name, scale=1.0):
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

    def draw_with_pulse(self, surface, size=20, time=15):
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

    def set_bgs(self, bgs, weight, k=10):
        self.bgs = random.choices(bgs, weights=weight, k=k)
        self.bgs_origin, self.cum_w, self.k = bgs, weight, k

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


class Text:
    def __init__(self, x, y, text='', scale=20, sound=None, color=(255, 255, 255), font="fonts/pxl_tactical.ttf",
                 set_topleft=False, set_midleft=False, set_midright=False, set_bottomleft=False, set_midbottom=False, set_bottomright=False):
        self.center = (x, y)
        self.scale = scale
        self.sound = sound
        self.color = color
        self.string = text
        self.font_path = font

        self.font = pg.font.Font(self.font_path, self.scale)
        self.text = self.font.render(self.string, False, self.color).convert_alpha()
        self.rect = self.text.get_rect()

        if set_topleft:
            self.rect.topleft = (x, y)
        elif set_midleft:
            self.rect.midleft = (x, y)
        elif set_midright:
            self.rect.midright = (x, y)
        elif set_bottomleft:
            self.rect.bottomleft = (x, y)
        elif set_midbottom:
            self.rect.midbottom = (x, y)
        elif set_bottomright:
            self.rect.bottomright = (x, y)
        else:
            self.rect.center = (x, y)

        self.on_button = False

        self.temporary_string = None

    def draw(self, surface, mp3_cut=False, color=None):
        if color:
            if mp3_cut:
                text = self.font.render(self.string[:-4], False, color).convert_alpha()
            else:
                text = self.font.render(self.string, False, color).convert_alpha()
            surface.blit(text, self.rect)
        else:
            if mp3_cut:
                text = self.font.render(self.string[:-4], False, self.color).convert_alpha()
                surface.blit(text, self.rect)
            else:
                surface.blit(self.text, self.rect)

    def draw_as_button(self, surface, block=False, surface_topleft=(0, 0), press_color=(255, 255, 200)):
        action = False
        x, y = surface_topleft
        if not block:
            pos = pg.mouse.get_pos()
            x_b = (pos[0] >= x) and (pos[0] <= x + surface.get_width())
            y_b = (pos[1] >= y) and (pos[1] <= y + surface.get_height())
            if self.rect.collidepoint((pos[0] - x, pos[1] - y)) and x_b and y_b:
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
        else:
            surface.blit(self.text, self.rect)

        return action

    def typing(self, surface, width=200, set_left=False, set_right=False):
        screen = pg.Surface((1280, 720)).convert_alpha()
        screen.blit(self.game.screen, (0, 0))

        typing = True
        while typing:
            if self.rect.width >= width:
                bar = pg.Surface((width, self.rect.height), pg.SRCALPHA).convert_alpha()
            else:
                bar = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA).convert_alpha()
            bar.fill((0, 0, 0, 255))

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DELETE and len(self.temporary_string) > 0:
                        self.temporary_string = self.temporary_string[:-1]
                    elif event.key == pg.K_ESCAPE:
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

    def draw(self, screen, speed=20, coordinates=(640, 360), set_topleft=False):
        current_time = pg.time.get_ticks()
        if current_time - self.last_update >= speed:
            self.last_update = current_time
            self.frame += 1
            if self.frame == len(self.gif):
                self.frame = 0

        if set_topleft:
            self.gif[self.frame].rect.topleft = coordinates
        else:
            self.gif[self.frame].rect.center = coordinates

        self.gif[self.frame].draw(screen)

    '''
    def fade(self, screen, speed, start_fade_time, time_to_fade=15):
        current_time = pg.time.get_ticks()
        if current_time - self.last_update >= speed:
            self.last_update = current_time
            self.frame += 1
            if self.frame == len(self.gif):
                self.frame = 0

        if int((pg.time.get_ticks() - start_fade_time) // time_to_fade) <= 255:
            faded_frame = self.gif[self.frame]
            faded_frame.image.set_alpha((int((pg.time.get_ticks() - start_fade_time) // time_to_fade)))
            faded_frame.draw(screen)
        else:
            self.fading = False
    '''


class Sheet:
    def __init__(self, image, scale=1):
        image = pg.image.load(image).convert_alpha()
        self.sheets = get_sheets(image, 3, scale)

        self.last_update = pg.time.get_ticks()
        self.frame = 0

    def draw(self, surface, coordinates=(640, 360), speed=100, set_topleft=False):
        current_time = pg.time.get_ticks()
        if current_time - self.last_update >= speed:
            self.last_update = current_time
            self.frame += 1
            if self.frame == len(self.sheets):
                self.frame = 0

        sheet_rect = self.sheets[self.frame].get_rect()

        if set_topleft:
            sheet_rect.topleft = coordinates
        else:
            sheet_rect.center = coordinates

        surface.blit(self.sheets[self.frame], sheet_rect)


class MusicPlayer:
    def __init__(self, path):
        self.path = path
        self.playlist = []
        self.others = []

        self.playing = False
        self.paused = False
        self.random_play = False
        self.loop = False
        self.MUSIC_END = pg.USEREVENT + 1
        pg.mixer.music.set_endevent(self.MUSIC_END)

        self.playlist = list((file_path, Text(400, 270, file, 20)) for file_path, file in settings.songs if
                             os.path.exists(file_path + file))

        self.others = list((file_path, Text(400, 270, file, 20)) for file_path, file in settings.others if
                           os.path.exists(file_path + file))

        self.covers = []
        self.load_covers()

        self.current_cover = None
        if self.playlist or self.others:
            self.change_cover()

        self.running_string_x = 0
        self.running_update = pg.time.get_ticks()

    def play(self):
        if not self.playing and not self.paused and (self.playlist or self.others):
            self.playing = True
            if settings.song_number < len(self.playlist):
                path = self.playlist[settings.song_number][0]
                file = self.playlist[settings.song_number][1].string
            else:
                path = self.others[settings.song_number - len(self.playlist)][0]
                file = self.others[settings.song_number - len(self.playlist)][1].string
            try:
                pg.mixer.music.load(path + file)
            except pygame.error:
                self.playlist = list((file_path, Text(400, 270, file, 20)) for file_path, file in settings.songs if
                                     os.path.exists(file_path + file))
                self.others = list((file_path, Text(400, 270, file, 20)) for file_path, file in settings.others if
                                   os.path.exists(file_path + file))
            pg.mixer.music.play()
            self.change_cover()
        elif not self.paused and (self.playlist or self.others):
            self.paused = True
            pg.mixer.music.pause()
        elif self.paused and (self.playlist or self.others):
            self.paused = False
            pg.mixer.music.unpause()

    def pause(self):
        pg.mixer.music.pause()

    def next(self):
        self.playing = False
        if self.random_play:
            settings.song_number = random.randrange(0, len(self.playlist) - 1)
        else:
            settings.song_number += 1
            if settings.song_number == len(self.playlist) + len(self.others) or settings.song_number >= len(self.playlist):
                settings.song_number = 0
        self.play()

    def prev(self):
        self.playing = False
        if self.random_play:
            settings.song_number = random.randrange(0, len(self.playlist) - 1)
        else:
            settings.song_number -= 1
            if settings.song_number < 0:
                settings.song_number = len(self.playlist) + len(self.others) - 1
            elif settings.song_number >= len(self.playlist):
                settings.song_number = 0
        self.play()

    def get_songs(self):
        return self.playlist

    def get_others(self):
        return self.others

    def set_volume(self):
        pg.mixer.music.set_volume(settings.music_volume)

    def choose_dir(self):
        path = filedialog.askdirectory(title="Choosing directory", initialdir="Desktop")
        if path:
            self.path = path + '/'
            self.refresh()
            self.clean_covers()
            self.load_covers()
            settings.song_number = 0

    def choose_song(self):
        file = filedialog.askopenfilename(title="Choosing directory")
        if file:
            path, name = "/".join(file.split("/")[:-1]) + "/", file.split("/")[-1]
            self.others.append((path, Text(400, 270, name, 20)))

    def pop_from_playlist(self, song):
        if self.playlist.index(song) == settings.song_number:
            settings.song_number = len(self.others) + len(self.playlist) - 1
        elif self.playlist.index(song) < settings.song_number:
            settings.song_number -= 1
        self.playlist.remove(song)
        self.others.append(song)

    def pop_from_others(self, song):
        if self.others.index(song) + len(self.playlist) == settings.song_number:
            settings.song_number = len(self.playlist)
        elif self.others.index(song) + len(self.playlist) > settings.song_number:
            settings.song_number += 1 * (len(self.playlist) <= settings.song_number)
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
            (self.path, Text(400, 270, file, 20)) for file in sorted(os.listdir(self.path)) if ".mp3" in file)
        settings.song_number = 0
        self.others = []
        self.save_to_settings()

    def draw_current_song(self, surface, coordinates, scale=0.5, set_topleft=False, set_bottomleft=False):
        if self.playing and self.playlist or self.others:
            song_name, cover = self.current_cover

            if set_topleft:
                cover.rect.topleft = coordinates
            elif set_bottomleft:
                cover.rect.bottomleft = coordinates
            else:
                cover.rect.center = coordinates

            song_names = [Text(5, cover.rect.bottomright[1], song_name, int(scale * 40), set_bottomleft=True),
                          Text(0, 0, song_name, int(scale * 40)),
                          Text(0, 0, song_name, int(scale * 40))
                          ]

            bar = pg.Surface((200, song_names[0].rect.height), pg.SRCALPHA).convert_alpha()
            bar.fill((0, 0, 0, 0))
            bar_rect = bar.get_rect()
            bar_rect.bottomleft = cover.rect.bottomright[0] + 10, cover.rect.bottomright[1]

            song_names[0].rect.midright = self.running_string_x, bar_rect.height // 2
            song_names[1].rect.midright = self.running_string_x - song_names[0].rect.width - 10, bar_rect.height // 2
            song_names[2].rect.midright = self.running_string_x - song_names[1].rect.width - 10, bar_rect.height // 2

            if pg.time.get_ticks() - self.running_update >= 100:
                self.running_string_x += 5
                self.running_update = pg.time.get_ticks()

            if song_names[2].rect.midleft[0] >= bar_rect.width:
                self.running_string_x = 0

            for song in song_names:
                bar.blit(song.text, song. rect)
            cover.draw(surface)
            surface.blit(bar, bar_rect)

    def change_cover(self, scale=0.1):
        tracks = self.playlist + self.others
        song_name = tracks[settings.song_number][1].string[:-4]
        for cover in self.covers:
            if song_name in cover[0].string:
                cover_img = Picture(0, 0, cover[1])
                cover_img.resize(80, 80)
                self.current_cover = (song_name, cover_img)
                break

    def clean_covers(self):
        for cover in sorted(os.listdir("audio/music/covers/")):
            if cover[-4:] == ".png" and cover != "default.png":
                os.remove("audio/music/covers/" + cover)

    def load_covers(self):
        for path, song in self.playlist + self.others:
            audiofile = eyed3.load(path + song.string)
            for image in audiofile.tag.images:
                if image:
                    with open('audio/music/covers/' + song.string[:-4] + '.png', 'wb+') as f:
                        f.write(image.image_data)
                    self.covers.append((song, 'audio/music/covers/' + song.string[:-4] + '.png'))
            self.covers.append((song, 'audio/music/covers/' + 'default.png'))


class PlayerStats:
    def __init__(self, coins_scale=4):

        self.coins_scale = coins_scale
        self.coins_image = pg.image.load("images/HUD/coins/MonedaD.png").convert_alpha()
        self.coins_sheets = get_sheets(self.coins_image, 5, self.coins_scale)
        self.frame = 0

        self.level_bar = []
        for file in sorted(os.listdir("images/HUD/level/")):
            if file[-4:] == ".png":
                self.level_bar.append(Picture(640, 360, "images/HUD/level/" + file, scale=2))

        self.start_level = 1000
        self.delta_level = 100

        self.last_update_time_in_game = 0

        self.last_update = pg.time.get_ticks()

    def draw_coins(self, surface, coordinates, time=250, set_topleft=False, set_midright=False):
        current_time = pg.time.get_ticks()
        if current_time - self.last_update >= time:
            self.frame += 1
            self.last_update = current_time
            if self.frame == len(self.coins_sheets):
                self.frame = 0

        coin_rect = self.coins_sheets[self.frame].get_rect()

        if set_topleft:
            coin_rect.topleft = coordinates
        else:
            coin_rect.center = coordinates

        coin_val = Text(coin_rect.midright[0] + 5, coin_rect.midright[1], str(settings.player_stats["coins"]),
                        self.coins_scale * 10, set_midleft=True)

        if set_midright:
            coin_rect.midright = coin_rect.midright[0] + (coordinates[0] - coin_val.rect.midright[0]), coordinates[1]
            coin_val = Text(coin_rect.midright[0] + 5, coin_rect.midright[1], str(settings.player_stats["coins"]),
                            self.coins_scale * 10, set_midleft=True)

        surface.blit(self.coins_sheets[self.frame], coin_rect)
        surface.blit(coin_val.text, coin_val.rect)

    def draw_level(self, surface, coordinates, set_topleft=False, set_midright=False, set_topright=False):
        start_level = self.start_level
        delta_level = self.delta_level

        max_score = start_level + delta_level * settings.player_stats["level"]

        curr_score = settings.player_stats["score"] - (
                (start_level + (start_level + delta_level * (settings.player_stats["level"] - 1))) *
                settings.player_stats["level"]) // 2

        score = Text(0, 0, "LVL: " + str(settings.player_stats["level"]) + " - " + str(curr_score) + "/" + str(max_score), 20)

        curr_level = 0
        while curr_level * (max_score / len(self.level_bar)) < curr_score:
            curr_level += 1

        if set_topleft:
            self.level_bar[curr_level].rect.topleft = coordinates
        elif set_midright:
            self.level_bar[curr_level].rect.midright = coordinates
        elif set_topright:
            self.level_bar[curr_level].rect.topright = coordinates
        else:
            self.level_bar[curr_level].rect.center = coordinates

        score.rect.topright = self.level_bar[curr_level].rect.bottomright[0], self.level_bar[curr_level].rect.bottomright[1] + 10

        self.level_bar[curr_level].draw(surface)
        score.draw(surface)

    def increase_score(self, value):
        start_level = self.start_level
        delta_level = self.delta_level
        max_score = ((start_level + (start_level + delta_level * settings.player_stats["level"])) *
                     (settings.player_stats["level"] + 1)) // 2
        settings.player_stats["score"] += value
        curr_score = settings.player_stats["score"]
        if curr_score >= max_score:
            settings.player_stats["level"] += 1
            return self.increase_score(0)
        return 0

    def increase_coins(self, value):
        settings.player_stats["coins"] += value

    def decrease_coins(self, value):
        if settings.player_stats["coins"] - value >= 0:
            settings.player_stats["coins"] -= value
            return 1
        return 0

    def update_time_in_game(self):
        settings.player_stats["time_in_game"] += pg.time.get_ticks() - self.last_update_time_in_game
        self.last_update_time_in_game = pg.time.get_ticks()

    def get_time_in_game(self):
        self.update_time_in_game()
        time = settings.player_stats["time_in_game"]
        return f'{(time // 86400000):03}' + ":" + f'{((time % 86400000) // 3600000):02}' + ":" + f'{((time % 3600000) // 60000):02}'
