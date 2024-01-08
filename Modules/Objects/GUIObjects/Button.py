import pygame as pg


class Button:
    def __init__(self, image_off_name, image_on_name, sound=None, scale=1):
        self.image_off = pg.image.load(image_off_name).convert_alpha()
        self.image_on = pg.image.load(image_on_name).convert_alpha()

        self.click_sound = sound

        # FOR NON-PUSHED BUTTON

        width_off = self.image_off.get_width()
        height_off = self.image_off.get_height()
        self.image_off = pg.transform.scale(self.image_off, (int(width_off * scale), int(height_off * scale)))
        self.rect = self.image_off.get_rect()

        # FOR PUSHED BUTTON

        width_on = self.image_on.get_width()
        height_on = self.image_on.get_height()
        self.image_on = pg.transform.scale(self.image_on, (int(width_on * scale), int(height_on * scale)))

        # FOR BUTTON PUSHING

        self.on_button = False

    def draw(self, surface, coordinates, block=False, surface_topleft=(0, 0), position="center"):
        setattr(self.rect, position, coordinates)
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
