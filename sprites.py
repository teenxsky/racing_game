import pygame as pg
import random
import math
from settings import *


class Car(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image_loaded = pg.image.load(image).convert_alpha()

        image_scale = 45 / self.image_loaded.get_rect().width
        new_width = self.image_loaded.get_rect().width * image_scale
        new_height = self.image_loaded.get_rect().height * image_scale

        self.image = pg.transform.scale(self.image_loaded, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Enemy:
    def __init__(self, image):
        self.image = pg.image.load(image).convert_alpha()
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(300, 980)
        self.rect.y = random.randrange(-200, -100)
        self.speed = 0

    def set_speed(self, speed):
        self.speed = speed

    def move(self, surface):
        self.rect.move_ip(0, self.speed)
        if self.rect.y > 720 and self.rect.topright[1] > 720:
            self.rect.x = random.randrange(300, 900)
            self.rect.y = -150

        surface.blit(self.image, self.rect)


class Player:
    def __init__(self, image, x, y):
        # super().__init__(self, image)
        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0
        self.max_speed = 30

        self.rotation_vel = 0.3
        self.vel = 0.1
        self.max_vel = 20
        self.angle = 0
        self.acceleration = 0.1
        self.reduce_vel = 0.5
        self.vel_of_forward = 0.01
        self.vel_of_horizontal_stop = 1
        self.horizontal = 1
        self.moving_lr_vel = 0.003

        self.screen = None

    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed

    def move(self, screen):
        keys = pg.key.get_pressed()
        self.screen = screen

        if self.angle != 0 and not keys[settings.KEYS["MOVE LEFT"]] and not keys[settings.KEYS["MOVE RIGHT"]]:
            if self.angle > 0:
                self.angle -= self.rotation_vel
                if math.radians(self.angle) > 0.2:
                    self.rotation_vel *= 1.2
                else:
                    self.rotation_vel /= 1.2

                '''self.rect.x -= self.horizontal
                self.horizontal /= 1.01'''
                #self.mathematical_calculations(Forward=False)

            if self.angle < 0:
                self.angle += self.rotation_vel
                if math.radians(self.angle) < -0.2:
                    self.rotation_vel *= 1.2
                else:
                    self.rotation_vel /= 1.2

                '''self.rect.x -= self.horizontal
                self.horizontal /= 1.01'''

            if 0 < self.angle < 1:
                self.angle = 0
                self.rotation_vel = 0.1
                #self.mathematical_calculations(Forward=False)

        elif keys[settings.KEYS["MOVE LEFT"]]:
            if math.radians(self.angle + self.rotation_vel) < 0.4:
                self.angle += self.rotation_vel
                if math.radians(self.angle) < 0.2:
                    self.rotation_vel *= 1.2
                else:
                    self.rotation_vel /= 1.2
                # if self
                # self.moving_lr_vel *= 1.2
            # self.vel = min(self.vel + self.acceleration, self.max_vel)

            self.mathematical_calculations(Left=True)

        elif keys[settings.KEYS["MOVE RIGHT"]]:
            if math.radians(self.angle + self.rotation_vel) > -0.4:
                self.angle -= self.rotation_vel
                if math.radians(self.angle) > -0.2:
                    self.rotation_vel *= 1.2
                else:
                    self.rotation_vel /= 1.2
            self.vel = min(self.vel + self.acceleration, self.max_vel)
            self.mathematical_calculations(Right=True)

        elif keys[settings.KEYS["MOVE UP"]]:
            if self.rect.x < 150:
                self.vel_of_forward *= 1.2
            else:
                self.vel_of_forward /= 1.2
            self.speed = min(self.speed + self.acceleration, self.max_speed)
            self.mathematical_calculations(Forward=True)

        else:
            self.vel = max(self.vel - self.acceleration, 0)
            self.mathematical_calculations(SoftBack=True)

    def mathematical_calculations(self, Forward=False, Back=False, Left=False, Right=False, SoftBack=False):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel_of_forward
        self.horizontal = 0

        if Forward and self.rect.y > 20:
            if self.speed >= self.max_speed:
                self.rect.y -= self.speed
            self.reduce_vel = self.speed

        if SoftBack and 515 >= self.rect.y + self.speed >= 20:
            self.rect.y += self.speed
            self.speed /= 1.01
            self.vel_of_horizontal_stop = 1

        if 365 <= self.rect.x <= 850 and self.speed != 0:
            if self.rect.x - self.horizontal > 850:
                self.rect.x = 850
            elif self.rect.x - self.horizontal < 365:
                self.rect.x = 365
            elif Left:
                self.rect.x -= self.moving_lr_vel

    def blit_rotate_center(self, screen):
        rotated_image = pg.transform.rotate(self.image, self.angle + 180)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.rect.x, self.rect.y)).center)
        screen.blit(rotated_image, new_rect.topleft)


'''    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.rect.move_ip(0, -1 * self.speed)

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    surface.blit(self.image, self.rect)
'''

'''if not moved:
    player_car.reduce_speed()

   if event.key == pg.K_UP:
        if self.rect.y > 20 and self.rect.topright[1] > 20:
            self.rect.move_ip(0, -1 * self.speed)
    if event.key == pg.K_DOWN:
        if self.rect.bottomleft[1] < 700 and self.rect.bottomright[1] < 700:
            self.rect.move_ip(0, self.speed)
    if event.key == pg.K_LEFT:
        if self.rect.x > 20 and self.rect.bottomleft[0] > 20:
            self.rect.move_ip(-1 * self.speed, 0)
    if event.key == pg.K_RIGHT:
        if self.rect.topright[1] < 1260 and self.rect.bottomright[1] < 1260:
            self.rect.move_ip(self.speed, 0)'''

# surface.blit(self.image, self.rect)
