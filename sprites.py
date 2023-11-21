import pygame as pg
import random
import math


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
        self.speed = 5

        self.rotation_vel = 4
        self.vel = 0
        self.max_vel = self.speed
        self.angle = 0
        self.acceleration = 2
        self.reduce_vel = self.speed

        self.screen = None

    def set_speed(self, speed):
        self.speed = speed

    def move(self, screen):
        # pressed_keys = pg.mouse.get_pressed()
        keys = pg.key.get_pressed()
        self.screen = screen

        if self.speed != 0:
            if keys[pg.K_a] or keys[pg.K_LEFT]:
                if math.radians(self.angle + self.rotation_vel) < 1.0472:
                    self.angle += self.rotation_vel
                self.vel = min(self.vel + self.acceleration, self.max_vel)
                self.mathematical_calculations(Forward=True)

            elif keys[pg.K_d] or keys[pg.K_RIGHT]:
                if math.radians(self.angle + self.rotation_vel) > -1.0472:
                    self.angle -= self.rotation_vel
                self.vel = min(self.vel + self.acceleration, self.max_vel)
                self.mathematical_calculations(Forward=True)

            elif keys[pg.K_w] or keys[pg.K_UP]:
                self.vel = min(self.vel + self.acceleration, self.max_vel)
                self.mathematical_calculations(Forward=True)

            else:
                self.vel = max(self.vel - self.acceleration / 5, 0)
                self.mathematical_calculations(Back=True)

        self.blit_rotate_center()

    def mathematical_calculations(self, Forward=False, Back=False):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        if Forward and self.rect.y > 0:
            self.rect.x -= horizontal
            self.rect.y -= vertical
            self.reduce_vel = self.speed
        if Back and self.rect.y < 500:
            self.rect.y += self.reduce_vel
            self.reduce_vel /= 1.01

    def blit_rotate_center(self):
        rotated_image = pg.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.rect.x, self.rect.y)).center)
        self.screen.blit(rotated_image, new_rect.topleft)


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
