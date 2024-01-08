import pygame as pg


class Picture:
    def __init__(self, image_name, scale):
        self.image = pg.image.load(image_name).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()

        if isinstance(scale, tuple):
            self.image = pg.transform.scale(self.image, scale)
        else:
            self.image = pg.transform.scale(self.image, (width * scale, height * scale))

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()

        self.current_size = 0
        self.pulse = True

        self.last_update = pg.time.get_ticks()

    def draw(self, surface, coordinates, block=False, surface_topleft=(0, 0), position="center"):
        setattr(self.rect, position, coordinates)
        action = False
        x, y = surface_topleft
        if not block:
            pos = pg.mouse.get_pos()
            x_b = (pos[0] >= x) and (pos[0] <= x + surface.get_width())
            y_b = (pos[1] >= y) and (pos[1] <= y + surface.get_height())
            if self.rect.collidepoint((pos[0] - x, pos[1] - y)) and x_b and y_b:
                action = True
        surface.blit(self.image, self.rect)
        return action

    def draw_with_pulse(self, surface, coordinates, size=20, time=15, position="center"):
        setattr(self.rect, position, coordinates)
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
