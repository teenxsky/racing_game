import pygame as pg
import random


class Car(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pg.image.load(image).convert_alpha()
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()


class Enemy:
    def __init__(self, image):
        #super().__init__(self, image)
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
            self.rect.x = random.randrange(300, 980)
            self.rect.y = random.randrange(-200, -100)

        surface.blit(self.image, self.rect)


class Player(Car):
    def __init__(self, image, x, y):
        #super().__init__(self, image)
        self.image = pg.image.load(image).convert_alpha()
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0

    def set_speed(self, speed):
        self.speed = speed

    def move(self, surface):
        #pressed_keys = pg.mouse.get_pressed()

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
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
                        self.rect.move_ip(self.speed, 0)

        surface.blit(self.image, self.rect)


