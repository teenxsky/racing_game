import pygame as pg
import random


class Picture:
    def __init__(self, image_name, scale=1):
        self.image = pg.image.load(image_name).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pg.transform.scale(self.image, (int(width * scale), int(height * scale)))
        self.image_rect = self.image.get_rect()












def music_change(playList, current_song):
    next_song = random.choice(playList)
    while current_song == next_song:
        next_song = random.choice(playList)
    pg.mixer.music.load(next_song)
    pg.mixer.music.play()
    current_song = next_song


