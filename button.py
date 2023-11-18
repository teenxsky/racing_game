import pygame as pg


class Button:
    def __init__(self, x, y, image_off, image_on, sound, scale):
        self.click_sound = sound
        width_off = image_off.get_width()
        height_off = image_off.get_height()
        self.image_off = pg.transform.scale(image_off, (int(width_off * scale), int(height_off * scale)))
        self.rect_off = self.image_off.get_rect()
        self.rect_off.topleft = (x, y)
        if image_on:
            width_on = image_on.get_width()
            height_on = image_on.get_height()
            self.image_on = pg.transform.scale(image_on, (int(width_on * scale), int(height_on * scale)))
            self.rect_on = self.image_on.get_rect()
            self.rect_on.topleft = (x, y)
        else:
            self.image_on = self.image_off
            self.rect_on = self.rect_off
            self.rect_on.topleft = (x, y)

        self.mouse_off, self.mouse_on = False, False
        self.clicked = False
        self.on_button = False

    def draw(self, surface):
        action = False

        pos = pg.mouse.get_pos()

        if self.rect_off.collidepoint(pos) or self.rect_on.collidepoint(pos):
            self.mouse_off = True
            self.mouse_on = False
            if not self.on_button:
                self.click_sound.play()
            self.on_button = True
            if pg.mouse.get_pressed()[0] and not self.clicked:
                action = True
        else:
            self.mouse_off = False
            self.mouse_on = True
            self.on_button = False

        if not pg.mouse.get_pressed()[0]:
            self.clicked = False

        if self.mouse_off:
            surface.blit(self.image_on, (self.rect_on.x, self.rect_on.y))
        else:
            surface.blit(self.image_off, (self.rect_off.x, self.rect_off.y))

        return action


class Picture(Button):
    def __init__(self, x, y, image_off, scale=1):
        Button.__init__(self, x, y, image_off, None, None, scale)
        self.current_size = 0
        self.state = False

    def draw_with_anim(self, surface, size):
        if not self.state:
            self.current_size += 1
            new_width = self.image_off.get_width() + 1
            new_height = self.image_off.get_height() + 1
            self.image_off = pg.transform.scale(self.image_on, (new_width, new_height))
            rect = self.image_off.get_rect(center=self.rect_off.topleft)
            if self.current_size == size:
                self.state = True
            surface.blit(self.image_off, rect)
        else:
            self.current_size -= 1
            new_width = self.image_off.get_width() - 1
            new_height = self.image_off.get_height() - 1
            self.image_off = pg.transform.scale(self.image_on, (new_width, new_height))
            rect = self.image_off.get_rect(center=self.rect_off.topleft)
            if self.current_size == 0:
                self.state = False
            surface.blit(self.image_off, rect)


