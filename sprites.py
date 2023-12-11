import pygame as pg
import random
import math
from settings import *


class Vehicle(pg.sprite.Sprite):
    def __init__(self, x, y, image):
        pg.sprite.Sprite.__init__(self)

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerVehicle(Vehicle):
    def __init__(self, x, y, image_in):
        image = image_in
        super().__init__(x, y, image)


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
    def __init__(self, enemies, enemy_speed, main_speed):
        self.images = [sprite.image for sprite in enemies]
        self.rect = enemies[0].rect
        self.rect.x = random.randrange(250, 950)
        self.rect.y = -300

        self.enemy_speed = enemy_speed
        self.main_speed = main_speed

        self.last_update = pg.time.get_ticks()
        self.frame = 0

        self.mask = None

        self.render = True

    def render_enemies(self, state=True):
        if state:
            self.render = True
        else:
            self.render = False

    def set_speed(self, enemy_speed=None, main_speed=None):
        if enemy_speed is not None:
            self.enemy_speed = enemy_speed
        if main_speed is not None:
            self.main_speed = main_speed

    def get_const(self, x=False, y=False, mask=False):
        if x:
            return self.rect.x
        if y:
            return self.rect.y
        if mask:
            return self.mask

    def move(self, surface):
        if not self.render and self.rect.y == -300:
            pass
        else:
            self.rect.move_ip(0, self.enemy_speed + self.main_speed)
            if self.rect.y > 720 and self.rect.topright[1] > 720:
                self.rect.x = random.randrange(250, 950)
                self.rect.y = -300

            current_time = pg.time.get_ticks()
            if current_time - self.last_update >= 100 and self.enemy_speed != 0:
                self.last_update = current_time
                self.frame += 1
                if self.frame == len(self.images):
                    self.frame = 0

            self.mask = pg.mask.from_surface(self.images[self.frame])

            surface.blit(self.images[self.frame], (self.rect.x, self.rect.y))


class Player:
    def __init__(self, player):
        self.images = [sprite.image for sprite in player]
        self.mask = None
        self.rect = player[0].rect
        self.min_y = self.rect.y

        self.speed = 0
        self.max_speed = 30

        self.rotation_vel = 0.3
        self.angle = 0
        self.acceleration = 0.1

        self.moving_lr_vel = 0
        self.speed_is_max = False
        self.vel_of_forward = -1

        self.press_left = 0
        self.press_right = 0
        self.press_up = 0
        self.press_down = 0
        self.count_soft_back = 0

        self.screen = None
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.update_rate = 100

        self.state_collision = False

    def collision(self, state=False):
        if state:
            self.acceleration = 0.2
            self.state_collision = True
        else:
            self.acceleration = 0.1
            self.state_collision = False
            self.angle = 0

    def set_const(self, speed=None, angle=None, update_rate=None):
        if speed is not None:
            self.speed = speed
        if angle is not None:
            self.angle = angle
        if update_rate is not None:
            self.update_rate = update_rate

    def get_const(self, speed=False, angle=False, x=False, y=False, mask=False):
        if speed:
            return self.speed
        if angle:
            return self.angle
        if x:
            return self.rect.x
        if y:
            return self.rect.y
        if mask:
            return self.mask

    def move(self, screen):
        keys = pg.key.get_pressed()
        self.screen = screen

        def left_reverse_animation():
            if self.angle > 0:
                self.angle -= self.rotation_vel
                if math.radians(self.angle) > 0.2:
                    self.rotation_vel *= 1.2
                else:
                    self.rotation_vel /= 1.001

            if -1 <= self.angle <= 1:
                self.angle = 0
                self.rotation_vel = 0.3
                self.moving_lr_vel = 0
            elif self.moving_lr_vel - 0.3 > 0:
                self.moving_lr_vel -= 0.3

            self.mathematical_calculations(Left=True)

        def right_reverse_animation():
            if self.angle < 0:
                self.angle += self.rotation_vel
                if math.radians(self.angle) < -0.2:
                    self.rotation_vel *= 1.2
                else:
                    self.rotation_vel /= 1.001

            if -1 <= self.angle <= 1:
                self.angle = 0
                self.rotation_vel = 0.3
                self.moving_lr_vel = 0
            elif self.moving_lr_vel - 0.3 > 0:
                self.moving_lr_vel -= 0.3

            self.mathematical_calculations(Right=True)

        def return_side_move():
            if self.angle != 0 and not keys[settings.KEYS["MOVE LEFT"]] and not keys[settings.KEYS["MOVE LEFT"]]:
                self.rotation_vel = 0.6
                self.press_left = 0
                self.press_right = 0

                if self.angle > 0:
                    left_reverse_animation()
                else:
                    right_reverse_animation()

        def left_animation():
            if 250 < self.rect.x <= 940:
                if self.speed != 0:
                    self.press_left += 1
                    if self.press_left == 1:
                        self.moving_lr_vel = 0
                        self.rotation_vel = 0.5

                    if math.radians(self.angle + self.rotation_vel) < 0.4:
                        self.angle += self.rotation_vel
                        if math.radians(self.angle) < 0.2:
                            self.rotation_vel *= 1.2
                        else:
                            self.rotation_vel /= 1.2
                    self.moving_lr_vel += 0.5
                    self.mathematical_calculations(Left=True)

        def right_animation():
            if 250 <= self.rect.x < 940:
                if self.speed != 0:
                    self.press_right += 1
                    if self.press_right == 1:
                        self.moving_lr_vel = 0
                        self.rotation_vel = 0.5

                    if math.radians(self.angle + self.rotation_vel) > -0.4:
                        self.angle -= self.rotation_vel
                        if math.radians(self.angle) > -0.2:
                            self.rotation_vel *= 1.2
                        else:
                            self.rotation_vel /= 1.2
                    self.moving_lr_vel += 0.5
                    self.mathematical_calculations(Right=True)

        def up_animation():
            if self.rect.y <= 50:
                self.rect.y = 50
            if self.speed_is_max and self.rect.y >= 50:
                self.press_up += 1
                if self.press_up == 1:
                    self.vel_of_forward = 0

                if self.rect.y <= 50:
                    self.rect.y = 50
                else:
                    self.vel_of_forward = min(self.vel_of_forward + 0.1, 10)
                    self.rect.y -= self.vel_of_forward
            else:
                self.speed = min(self.speed + self.acceleration, self.max_speed)

            if self.speed == self.max_speed:
                self.vel_of_forward = max(self.vel_of_forward, 0)
                self.speed_is_max = True

        def down_animation():
            if self.speed_is_max and self.rect.y + self.vel_of_forward <= self.min_y:
                self.press_down += 1
                if self.press_down == 1:
                    self.vel_of_forward = 15
                self.vel_of_forward = max(self.vel_of_forward - 0.1, 0)
                self.rect.y += self.vel_of_forward

                if self.rect.y >= self.min_y:
                    self.rect.y = self.min_y

                if self.rect.y == self.min_y:
                    self.vel_of_forward = -1
                    self.speed_is_max = False
            else:
                if self.speed - self.acceleration <= 0:
                    self.speed = 0
                else:
                    self.speed = min(self.speed - self.acceleration * 2, self.max_speed)

        def soft_back_animation():
            self.count_soft_back += 1
            self.press_up = 0
            self.press_down = 0

            if self.speed > 0:
                self.mathematical_calculations(SoftBack=True)

        if keys[settings.KEYS["MOVE UP"]] and keys[settings.KEYS["MOVE LEFT"]] and not self.state_collision:
            up_animation()
            left_animation()
        elif keys[settings.KEYS["MOVE UP"]] and keys[settings.KEYS["MOVE RIGHT"]] and not self.state_collision:
            up_animation()
            right_animation()
        elif keys[settings.KEYS["MOVE UP"]] and not self.state_collision:
            up_animation()
            return_side_move()
        elif keys[settings.KEYS["MOVE LEFT"]] and not self.state_collision:
            left_animation()
            soft_back_animation()
        elif keys[settings.KEYS["MOVE RIGHT"]] and not self.state_collision:
            right_animation()
            soft_back_animation()
        elif keys[settings.KEYS["MOVE DOWN"]] and not self.state_collision:
            down_animation()
            return_side_move()
        else:
            soft_back_animation()
            return_side_move()

    def mathematical_calculations(self, Left=False, Right=False, SoftBack=False):
        if 250 <= self.rect.x <= 940:
            if Left:
                if self.rect.x - self.moving_lr_vel < 250 or self.rect.x < 250:
                    self.rect.x = 250
                else:
                    self.rect.x -= self.moving_lr_vel
            elif Right:
                if self.rect.x + self.moving_lr_vel > 940 or self.rect.x > 940:
                    self.rect.x = 940
                else:
                    self.rect.x += self.moving_lr_vel

        if SoftBack and 49 <= self.rect.y <= self.min_y:
            if self.speed_is_max:
                if self.count_soft_back == 1:
                    self.vel_of_forward = 15

                self.vel_of_forward = max(self.vel_of_forward - self.acceleration, 0)
                self.rect.y += self.vel_of_forward

                if self.vel_of_forward < 1:
                    self.vel_of_forward += 1.5

                if self.rect.y + self.vel_of_forward > self.min_y or self.rect.y > self.min_y:
                    self.rect.y = self.min_y
                else:
                    self.vel_of_forward = max(self.vel_of_forward - self.acceleration, 0)
                    self.rect.y += self.vel_of_forward

                if self.rect.y == self.min_y:
                    self.vel_of_forward = -1
                    self.speed_is_max = False

            else:
                self.speed = max(self.speed - self.acceleration * 0.5, 0)

                if self.rect.y + self.speed > self.min_y or self.rect.y > self.min_y:
                    self.rect.y = self.min_y
                else:
                    self.rect.y += self.speed

    def blit_rotate_center(self, screen):
        current_time = pg.time.get_ticks()
        if (current_time - self.last_update >= self.update_rate) and (self.update_rate != 0):
            self.last_update = current_time
            self.frame += 1
            if self.frame == len(self.images):
                self.frame = 0

        rotated_image = pg.transform.rotate(self.images[self.frame], self.angle)
        new_rect = (self.rect.x, self.rect.y)
        self.mask = pg.mask.from_surface(rotated_image)

        screen.blit(rotated_image, new_rect)


'''    def move(self, screen):
        keys = pg.key.get_pressed()
        self.screen = screen
        self.previous_vel_of_forward = self.vel_of_forward
        print(self.speed_is_max)

        def left_reverse_animation():
            if self.angle > 0:
                self.angle -= self.rotation_vel
                if math.radians(self.angle) > 0.2:
                    self.rotation_vel *= 1.2
                else:
                    self.rotation_vel /= 1.001

            if -1 <= self.angle <= 1:
                self.angle = 0
                self.rotation_vel = 0.3
                self.moving_lr_vel = 0
            elif self.moving_lr_vel - 0.3 > 0:
                self.moving_lr_vel -= 0.3

            self.mathematical_calculations(Left=True)

        def right_reverse_animation():
            if self.angle < 0:
                self.angle += self.rotation_vel
                if math.radians(self.angle) < -0.2:
                    self.rotation_vel *= 1.2
                else:
                    self.rotation_vel /= 1.001

            if -1 <= self.angle <= 1:
                self.angle = 0
                self.rotation_vel = 0.3
                self.moving_lr_vel = 0
            elif self.moving_lr_vel - 0.3 > 0:
                self.moving_lr_vel -= 0.3

            self.mathematical_calculations(Right=True)

        if self.angle != 0 and not keys[settings.KEYS["MOVE LEFT"]] and not keys[settings.KEYS["MOVE RIGHT"]]:
            self.rotation_vel = 0.6
            self.press_left = 0
            self.press_right = 0

            if self.angle > 0:
                left_reverse_animation()
            else:
                right_reverse_animation()

        elif keys[settings.KEYS["MOVE LEFT"]]:
            if self.speed != 0:
                self.press_left += 1
                if self.press_left == 1:
                    self.moving_lr_vel = 0
                    self.rotation_vel = 0.5

                if math.radians(self.angle + self.rotation_vel) < 0.4:
                    self.angle += self.rotation_vel
                    if math.radians(self.angle) < 0.2:
                        self.rotation_vel *= 1.2
                    else:
                        self.rotation_vel /= 1.2
                self.moving_lr_vel += 0.5
                self.mathematical_calculations(Left=True)

        elif keys[settings.KEYS["MOVE RIGHT"]]:
            if self.speed != 0:
                self.press_right += 1
                if self.press_right == 1:
                    self.moving_lr_vel = 0
                    self.rotation_vel = 0.5

                if math.radians(self.angle + self.rotation_vel) > -0.4:
                    self.angle -= self.rotation_vel
                    if math.radians(self.angle) > -0.2:
                        self.rotation_vel *= 1.2
                    else:
                        self.rotation_vel /= 1.2
                self.moving_lr_vel += 0.5
                self.mathematical_calculations(Right=True)

        elif keys[settings.KEYS["MOVE UP"]]:
            if self.speed_is_max and self.rect.y >= 50:
                self.press_up += 1
                if self.press_up == 1:
                    self.vel_of_forward = 0

                if self.rect.y <= 50:
                    self.rect.y = 50
                else:
                    self.vel_of_forward = min(self.vel_of_forward + 0.1, 10)
                    self.rect.y -= self.vel_of_forward
            else:
                self.speed = min(self.speed + self.acceleration, self.max_speed)

            if self.speed == self.max_speed:
                self.vel_of_forward = max(self.vel_of_forward, 0)
                self.speed_is_max = True


        elif keys[settings.KEYS["MOVE DOWN"]]:
            if self.speed_is_max and self.rect.y + self.vel_of_forward <= self.min_y:
                self.vel_of_forward = max(self.vel_of_forward - 0.1, 0)
                self.rect.y += self.vel_of_forward

                if self.rect.y >= self.min_y:
                    self.rect.y = self.min_y

                if self.rect.y == self.min_y:
                    self.vel_of_forward = -1
                    self.speed_is_max = False
            else:
                if self.speed - self.acceleration <= 0:
                    self.speed = 0
                else:
                    self.speed = min(self.speed - self.acceleration, self.max_speed)

        else:
            self.press_up = 0
            self.press_down = 0

            if self.speed > 0:
                self.mathematical_calculations(SoftBack=True)

    def mathematical_calculations(self, Left=False, Right=False, SoftBack=False):
        if 250 <= self.rect.x <= 950 and self.speed != 0:
            if Left:
                if self.rect.x - self.moving_lr_vel < 250 or self.rect.x < 250:
                    self.rect.x = 250
                else:
                    self.rect.x -= self.moving_lr_vel
            elif Right:
                if self.rect.x + self.moving_lr_vel > 950 or self.rect.x > 950:
                    self.rect.x = 950
                else:
                    self.rect.x += self.moving_lr_vel

        if SoftBack and 50 <= self.rect.y <= self.min_y:
            if self.speed_is_max:
                self.vel_of_forward = max(self.vel_of_forward - 0.1, 0)
                self.rect.y += self.vel_of_forward

                if self.rect.y + self.vel_of_forward > self.min_y or self.rect.y > self.min_y:
                    self.rect.y = self.min_y
                else:
                    self.vel_of_forward = max(self.vel_of_forward - 0.1, 0)
                    self.rect.y += self.vel_of_forward

                if self.rect.y == self.min_y:
                    self.vel_of_forward = -1
                    self.speed_is_max = False
            else:
                self.speed -= self.acceleration * 0.75
                if self.rect.y + self.speed > self.min_y or self.rect.y > self.min_y:
                    self.rect.y = self.min_y
                else:
                    self.rect.y += self.speed

    def blit_rotate_center(self, screen):
        rotated_image = pg.transform.rotate(self.image, self.angle + 180)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.rect.x, self.rect.y)).center)
        screen.blit(rotated_image, new_rect.topleft)'''
