from .Picture import Picture
from Modules.Objects.APIObjects.Settings import config
import random

SCREEN_WIDTH, SCREEN_HEIGHT = config.SCREEN_SIZE


class Background(Picture):
    def __init__(self, image_name, scale=1):
        super().__init__(image_name, scale)

        self.bg_y = 0

        self.bgs = []
        self.bgs_origin, self.cum_w, self.k = [], 0, 0
        self.scrolls = 0
        self.last_bg = self

    def scroll(self, surface, speed):
        self.bg_y += speed
        surface.blit(self.image, (0, self.bg_y))
        surface.blit(self.image, (0, self.bg_y - SCREEN_HEIGHT))
        if self.bg_y == SCREEN_HEIGHT:
            self.bg_y = 0

    def set_bgs(self, bgs, weight, k=10):
        self.bgs = random.choices(bgs, weights=weight, k=k)
        self.bgs_origin, self.cum_w, self.k = bgs, weight, k

    def random_scroll(self, surface, speed):
        self.bg_y += speed

        if self.scrolls == 0:
            surface.blit(self.last_bg.image, (0, self.bg_y))
            surface.blit(self.bgs[self.scrolls].image, (0, self.bg_y - surface.get_height()))
        else:
            surface.blit(self.bgs[self.scrolls - 1].image, (0, self.bg_y))
            surface.blit(self.bgs[self.scrolls].image, (0, self.bg_y - surface.get_height()))

        if (self.scrolls == len(self.bgs) - 1) and (self.bg_y >= surface.get_height()):
            self.last_bg = self.bgs[self.scrolls]
            self.set_bgs(self.bgs_origin, self.cum_w, self.k)
            self.scrolls = -1

        if self.bg_y >= surface.get_height():
            self.bg_y = 0
            self.scrolls += 1
