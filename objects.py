import pygame as pg
from PIL import Image

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
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
        else:
            self.mouse_off = False
            self.mouse_on = True
            self.on_button = False

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if self.mouse_off:
            surface.blit(self.image_on, (self.rect_on.x, self.rect_on.y))
        else:
            surface.blit(self.image_off, (self.rect_off.x, self.rect_off.y))

        return action


class Picture:
    def __init__(self, x, y, image, scale=1):
        self.coords = (x, y)
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pg.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.current_size = 0
        self.state_pulse = False

        self.frames_list = []

    def resize(self, width, height):
        self.image = pg.transform.scale(self.image, (width, height))

    def draw_just(self, surface):
        surface.blit(self.image, self.rect)

    def draw_with_pulse(self, surface, size, delta=1):
        if not self.state_pulse:
            self.current_size += delta
            new = self.width + self.current_size, self.height + self.current_size
            current_image = pg.transform.scale(self.image, new)
            current_rect = current_image.get_rect(center=self.rect.center)
            surface.blit(current_image, current_rect)
            if self.current_size >= size:
                self.state_pulse = True
        else:
            self.current_size -= delta
            new = self.width + self.current_size, self.height + self.current_size
            current_image = pg.transform.scale(self.image, new)
            current_rect = current_image.get_rect(center=self.rect.center)
            surface.blit(current_image, current_rect)
            if self.current_size <= 0:
                self.state_pulse = False

'''    def extractFrames(self, image_object):
        image = Image.open(image_object)
        for frame_numer in range(0, 5):
            image.seek(self.frames_list[frame])'''


'''class Vehicle(pg.sprite.Sprite):

    def __init__(self, image, x, y):
        pg.sprite.Sprite.__init__(self)

        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pg.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerVehicle(Vehicle):

    def __init__(self, pic, x, y):
        image = pic
        super().__init__(image, x, y)'''