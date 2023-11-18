import pygame as pg
import random


def music_change(playList, current_song):
    next_song = random.choice(playList)
    while current_song == next_song:
        next_song = random.choice(playList)
    pg.mixer.music.load(next_song)
    pg.mixer.music.play()
    current_song = next_song


