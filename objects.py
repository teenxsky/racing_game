import pygame as pg


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
        self.image = pg.image.load(image_name).convert_alpha()

        self.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.image = pg.transform.scale(self.image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = self.center

        self.current_size = 0

        # FOR JUMPING GAME TITLE

        self.state_pulse = False

    def resize(self, width, height):
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def draw_with_pulse(self, surface, size, delta=1):  # FOR JUMPING GAME TITLE
        if not self.state_pulse:
            self.current_size += delta
            new = self.width + self.current_size, self.height + self.current_size
            if self.current_size >= size:
                self.state_pulse = True
        else:
            self.current_size -= delta
            new = self.width + self.current_size, self.height + self.current_size
            if self.current_size <= 0:
                self.state_pulse = False
        current_image = pg.transform.scale(self.image, new)
        current_rect = current_image.get_rect(center=self.rect.center)
        surface.blit(current_image, current_rect)


class Text:
    def __init__(self, x, y, text, scale=20):
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
