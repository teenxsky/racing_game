import pygame as pg


class Button:
    def __init__(self, x, y, image_off_name, image_on_name, sound, scale=1):
        self.image_off = pg.image.load(image_off_name).convert_alpha()
        self.image_on = pg.image.load(image_on_name).convert_alpha()

        self.click_sound = sound

        width_off = self.image_off.get_width()
        height_off = self.image_off.get_height()
        self.image_off = pg.transform.scale(self.image_off, (int(width_off * scale), int(height_off * scale)))
        self.rect_off = self.image_off.get_rect()
        self.rect_off.center = (x, y)

        width_on = self.image_on.get_width()
        height_on = self.image_on.get_height()
        self.image_on = pg.transform.scale(self.image_on, (int(width_on * scale), int(height_on * scale)))
        self.rect_on = self.image_on.get_rect()
        self.rect_on.center = (x, y)

        self.on_button = False

    def draw(self, surface, block):
        action = False

        if not block:
            pos = pg.mouse.get_pos()
            if self.rect_off.collidepoint(pos):
                surface.blit(self.image_on, (self.rect_on.x, self.rect_on.y))
                if pg.mouse.get_pressed()[0] == 1:
                    action = True
                self.on_button = True
            else:
                surface.blit(self.image_off, (self.rect_off.x, self.rect_off.y))
                self.on_button = False

        else:
            surface.blit(self.image_off, (self.rect_off.x, self.rect_off.y))

        #if self.on_button:
        #    self.click_sound.play()

        return action


class Picture:
    def __init__(self, x, y, image_name, scale=1):
        self.image = pg.image.load(image_name).convert_alpha()

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.image = pg.transform.scale(self.image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y  # coordinates

        self.current_size = 0
        self.state_pulse = False

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


class Text:
    def __init__(self, x, y, text, scale):
        font = pg.font.Font("fonts/pxl_tactical.ttf", scale)
        self.text = font.render(text, False, (255, 255, 255)).convert_alpha()
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.text, self.text_rect)


class Background(Picture):
    def __init__(self, image_name, scale=1):
        super().__init__(0, 0, image_name, scale)
        self.bg_y = 0

    def scroll(self, surface, speed):
        self.bg_y += speed
        surface.blit(self.image, (0, self.bg_y))
        surface.blit(self.image, (0, self.bg_y - 720))
        if self.bg_y == 720:
            self.bg_y = 0
