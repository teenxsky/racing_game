from .Picture import Picture
import os
import pygame as pg


class GIF:
    def __init__(self, path, scale=1):
        self.path = path
        self.gif = []

        for file in sorted(os.listdir(self.path)):
            if ".DS_Store" not in file:
                self.gif.append(Picture(self.path + file, scale=scale))

        self.last_update = pg.time.get_ticks()
        self.frame = 0

    def draw(self, screen, speed=20, coordinates=(640, 360), position="center"):
        current_time = pg.time.get_ticks()
        if current_time - self.last_update >= speed:
            self.last_update = current_time
            self.frame += 1
            if self.frame == len(self.gif):
                self.frame = 0
        self.gif[self.frame].draw(screen, coordinates, position=position)

