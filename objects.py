import pygame as pg
from settings import *
import random
import os


class Button:
    def __init__(self, x, y, image_off_name, image_on_name, sound, scale=1):
        self.image_off = pg.image.load(image_off_name).convert_alpha()
        self.image_on = pg.image.load(image_on_name).convert_alpha()

        self.click_sound = sound

        # FOR NON-PUSHED BUTTON

        width_off = self.image_off.get_width()
        height_off = self.image_off.get_height()
        self.image_off = pg.transform.scale(self.image_off, (int(width_off * scale), int(height_off * scale)))
        self.rect_off = self.image_off.get_rect()
        self.rect_off.center = (x, y)

        # FOR PUSHED BUTTON

        width_on = self.image_on.get_width()
        height_on = self.image_on.get_height()
        self.image_on = pg.transform.scale(self.image_on, (int(width_on * scale), int(height_on * scale)))
        self.rect_on = self.image_on.get_rect()
        self.rect_on.center = (x, y)

        # FOR BUTTON PUSHING

        self.on_button = False

    def draw(self, surface, block):  # DRAW AND CHECKING IF MOUSE ON BUTTON
        action = False

        if not block:
            pos = pg.mouse.get_pos()
            if self.rect_off.collidepoint(pos) or self.rect_on.collidepoint(pos):
                if not self.on_button:
                    self.on_button = True
                    self.click_sound.play()

                surface.blit(self.image_on, (self.rect_on.x, self.rect_on.y))
                action = True
            else:
                self.on_button = False
                surface.blit(self.image_off, (self.rect_off.x, self.rect_off.y))

        else:
            surface.blit(self.image_off, (self.rect_off.x, self.rect_off.y))

        return action


class Picture:
    def __init__(self, x, y, image_name, scale=1):
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

    def draw_with_pulse(self, surface, size=20, time=15):  # FOR JUMPING GAME TITLE
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

    def set_bgs(self, bgs, cum_weight, k=10):
        self.bgs = random.choices(bgs, cum_weights=cum_weight, k=k)
        self.bgs_origin, self.cum_w, self.k = bgs, cum_weight, k

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


class HUD:
    def __init__(self, coins_size=1):
        coins_image = pg.image.load("images/HUD/coins/MonedaD.png").convert_alpha()
        self.coins_sheets = self.get_sheets(coins_image)
        self.frame = 0

        self.last_update = pg.time.get_ticks()

    def get_image(self, sheet, frame, scale=1, colour=(0, 0, 0)):
        width, height = sheet.get_height(), sheet.get_height()
        image = pg.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), ((frame * width), 0, width,height))
        image = pg.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image

    def get_sheets(self, image):
        sheets = []
        for i in range(image.get_width() // image.get_height()):
            sheets.append(self.get_image(image, i, 5))
        return sheets

    def draw_coins(self, surface, x, y, time): #Сделать в ХУД класс выведения коин или другого на экран со всеми примочками
        current_time = pg.time.get_ticks()

        coin_rect = self.coins_sheets[0].get_rect()
        coin_rect.center = (x, y)

        coin_val = Text(x + 70, y, str(settings.coins), 50)
        coin_val.rect.midleft = (coin_rect.midright[0] + 5, coin_rect.midright[1])

        surface.blit(self.coins_sheets[self.frame], coin_rect)
        surface.blit(coin_val.text, coin_val.rect)

        if current_time - self.last_update >= time:
            self.frame += 1
            self.last_update = current_time
            if self.frame == len(self.coins_sheets):
                self.frame = 0


class Text:
    def __init__(self, x, y, text='', scale=20, sound=None, color=(255, 255, 255)):
        self.center = (x, y)
        self.scale = scale
        self.sound = sound
        self.color = color
        self.string = text

        self.font = pg.font.Font("fonts/pxl_tactical.ttf", self.scale)
        self.text = self.font.render(self.string, False, self.color).convert_alpha()
        self.rect = self.text.get_rect()
        self.rect.center = (x, y)

        self.on_button = False

    def draw(self, surface):
        surface.blit(self.text, self.rect)

    def draw_as_button(self, surface, press_color=(255, 255, 200)):
        action = False
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
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

        return action

    def typing(self, surface):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DELETE and len(self.string) > 0:
                    self.string = self.string[:-1]
                else:
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

    def move(self, x, y):
        for frame in self.gif:
            frame.rect.center = (x, y)

    def draw(self, screen, speed=20):
        current_time = pg.time.get_ticks()
        if current_time - self.last_update >= speed:
            self.last_update = current_time
            self.frame += 1
            if self.frame == len(self.gif):
                self.frame = 0
        self.gif[self.frame].draw(screen)


#for row, line in enumerate(text)
