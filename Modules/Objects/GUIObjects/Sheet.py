import pygame as pg


def get_sheet(image, frames, scale=1):
    width, height = image.get_width(), image.get_height()
    sheets = []
    for frame in range(frames):
        image_area = pg.Surface(((width // frames), height)).convert_alpha()
        image_area.blit(image, (0, 0), ((frame * (width // frames)), 0, (width // frames), height))
        image_area = pg.transform.scale(image_area, ((width // frames) * scale, height * scale))
        image_area.set_colorkey((0, 0, 0))
        sheets.append(image_area)
    return sheets


class Sheet:
    def __init__(self, image, scale=1):
        image = pg.image.load(image).convert_alpha()
        self.sheets = get_sheet(image, 3, scale)

        self.last_update = pg.time.get_ticks()
        self.frame = 0

    def draw(self, surface, coordinates=(640, 360), speed=100, position="center"):
        current_time = pg.time.get_ticks()
        if current_time - self.last_update >= speed:
            self.last_update = current_time
            self.frame += 1
            if self.frame == len(self.sheets):
                self.frame = 0

        sheet_rect = self.sheets[self.frame].get_rect()
        setattr(sheet_rect, position, coordinates)
        surface.blit(self.sheets[self.frame], sheet_rect)
