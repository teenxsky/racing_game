import pygame as pg
import random
import math
from Modules.Objects.APIObjects.Settings import *


class Sprites(pg.sprite.Sprite):
    def __init__(self, x, y, image):
        pg.sprite.Sprite.__init__(self)

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerVehicle(Sprites):
    def __init__(self, x, y, image_in):
        super().__init__(x, y, image_in)


class OppVehicle(Sprites):
    def __init__(self, x, y, image_in):
        super().__init__(x, y, image_in)


class Elements(Sprites):
    def __init__(self, x, y, image_in):
        super().__init__(x, y, image_in)


class Explosion(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pg.image.load(f"Resources/Images/Hud/Explosion/exp{num}.png").convert_alpha()
            img = pg.transform.scale(img, (500, 500))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 5
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


class CoinsMechanics:
    def __init__(self, coins, coins_speed, type=None):
        self.type = type

        self.coins_images = [coins[i].image for i in range(len(coins))]
        self.rect = coins[0].rect
        self.rect.x = random.randrange(250, 950)
        self.rect.y = -300

        self.coins_speed = coins_speed

        self.time = pg.time.get_ticks()
        self.last_update = pg.time.get_ticks()
        self.frame = 0

        self.coins_mask = None

        self.coins_render = True

    def render(self, state=True):
        if state:
            self.coins_render = True
        else:
            self.coins_render = False

    def set_const(self, speed=None):
        if speed is not None:
            self.coins_speed = speed

    def get_const(self, x=False, y=False, mask=False):
        if x:
            return self.rect.x
        if y:
            return self.rect.y
        if mask:
            return self.coins_mask

    def move(self, screen):
        if not self.coins_render and self.rect.y == -300:
            pass
        else:
            current_time = pg.time.get_ticks()

            if self.type == "gold" or (self.type == "ruby" and current_time - self.time > 10000):
                if (self.type == "ruby" and current_time - self.time > 10000) and self.rect.y == -300:
                    self.time = pg.time.get_ticks()

                self.rect.move_ip(0, self.coins_speed)
                if self.rect.y > 720 and self.rect.topright[1] > 720:
                    self.rect.x = random.randrange(250, 950)
                    self.rect.y = -300

                current_time = pg.time.get_ticks()
                if current_time - self.last_update >= 100 and self.coins_speed != 0:
                    self.last_update = current_time
                    self.frame += 1
                    if self.frame == len(self.coins_images):
                        self.frame = 0

                self.coins_mask = pg.mask.from_surface(self.coins_images[self.frame])

                screen.blit(self.coins_images[self.frame], (self.rect.x, self.rect.y))


class OilMechanics:
    def __init__(self, oil, oil_speed):
        self.type = type

        self.oil_image = oil[0].image
        self.rect = oil[0].rect
        self.rect.x = random.randrange(500, 700)
        self.rect.y = -300

        self.oil_speed = oil_speed

        self.time = pg.time.get_ticks()

        self.oil_mask = None

        self.oil_render = True

    def render(self, state=True):
        if state:
            self.oil_render = True
        else:
            self.oil_render = False

    def set_const(self, speed=None):
        if speed is not None:
            self.oil_speed = speed

    def get_const(self, x=False, y=False, mask=False):
        if x:
            return self.rect.x
        if y:
            return self.rect.y
        if mask:
            return self.oil_mask

    def move(self, screen):
        if not self.oil_render and self.rect.y == -300:
            pass
        else:
            current_time = pg.time.get_ticks()

            if current_time - self.time > 30000:
                if current_time - self.time > 30000 and self.rect.y == -300:
                    self.time = pg.time.get_ticks()

                self.rect.move_ip(0, self.oil_speed)
                if self.rect.y > 720 and self.rect.topright[1] > 720:
                    self.rect.x = random.randrange(250, 950)
                    self.rect.y = -300

                self.oil_mask = pg.mask.from_surface(self.oil_image)

                screen.blit(self.oil_image, (self.rect.x, self.rect.y))


class Enemy:
    def __init__(self, enemies, enemy_speed, main_speed):
        self.images = [sprite.image for sprite in enemies]
        self.rect = enemies[0].rect
        self.rect.x = random.randrange(250, 950)
        self.rect.y = -300

        self.enemy_speed = enemy_speed
        self.main_speed = main_speed

        self.time = pg.time.get_ticks()
        self.last_update = pg.time.get_ticks()
        self.frame = 0

        self.mask = None

        self.render_enemy = True
        self.rendering_frequency = -1

        self.another_x = [-1, -1, -1]

    def render(self, state=True):
        if state:
            self.render_enemy = True
        else:
            self.render_enemy = False

    def set_speed(self, enemy_speed=None, main_speed=None, rendering_frequency=None, another_x=None):
        if enemy_speed is not None:
            self.enemy_speed = enemy_speed
        if main_speed is not None:
            self.main_speed = main_speed
        if rendering_frequency is not None:
            self.rendering_frequency = rendering_frequency
        if another_x is not None:
            for i in range(3):
                if self.another_x[i] != -1:
                    self.another_x[i] = another_x
                    break

    def get_const(self, x=False, y=False, mask=False):
        if x:
            return self.rect.x
        if y:
            return self.rect.y
        if mask:
            return self.mask

    def move(self, screen):
        if not self.render_enemy and self.rect.y == -300:
            pass
        else:
            current_time = pg.time.get_ticks()

            if current_time - self.time > self.rendering_frequency:
                if current_time - self.time > self.rendering_frequency and self.rect.y == -300:
                    self.time = pg.time.get_ticks()

                self.rect.move_ip(0, self.enemy_speed + self.main_speed)
                if self.rect.y > 720 and self.rect.topright[1] > 720:
                    self.rect.x = random.randrange(250, 950)
                    while self.another_x[0] - 120 > self.rect.x > self.another_x[0] + 120 and \
                            self.another_x[1] - 120 > self.rect.x > self.another_x[1] + 120 and \
                            self.another_x[2] - 120 > self.rect.x > self.another_x[2] + 120:
                        self.rect.x = random.randrange(250, 950)
                    self.rect.y = -300

                current_time = pg.time.get_ticks()
                if current_time - self.last_update >= 100 and self.enemy_speed != 0:
                    self.last_update = current_time
                    self.frame += 1
                    if self.frame == len(self.images):
                        self.frame = 0

                self.mask = pg.mask.from_surface(self.images[self.frame])

                screen.blit(self.images[self.frame], (self.rect.x, self.rect.y))


class Player:
    def __init__(self, player, max_speed, acceleration, change_moving_lr_vel):
        self.images = [sprite.image for sprite in player]
        self.mask = None
        self.rect = player[0].rect
        self.min_y = self.rect.y

        self.speed = 0
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.change_moving_lr_vel = change_moving_lr_vel

        self.rotation_vel = 0.3
        self.angle = 0
        self.arrow_angle = -15

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
            self.state_collision = True
        else:
            self.state_collision = False
            self.angle = 0

    def set_const(self, speed=None, angle=None, update_rate=None, y=None, vel_of_forward=None):
        if speed is not None:
            self.speed = speed
        if angle is not None:
            self.angle = angle
        if update_rate is not None:
            self.update_rate = update_rate
        if y is not None:
            self.rect.y = y
        if vel_of_forward is not None:
            self.vel_of_forward = vel_of_forward
    def get_const(self, speed=False, angle=False, x=False, y=False, mask=False, vel_of_forward=False):
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
        if vel_of_forward:
            return self.vel_of_forward

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
                    self.moving_lr_vel += self.change_moving_lr_vel
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
                    self.moving_lr_vel += self.change_moving_lr_vel
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
                    self.vel_of_forward = self.max_speed
                self.vel_of_forward = max(self.vel_of_forward - self.acceleration, 0)
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
                    self.speed = min(self.speed - self.acceleration * 1.2, self.max_speed)

        def soft_back_animation():
            self.count_soft_back += 1
            self.press_up = 0
            self.press_down = 0

            if self.speed > 0:
                self.mathematical_calculations(SoftBack=True)

        if keys[settings.KEYS["MOVE UP"]] and keys[settings.KEYS["MOVE LEFT"]]:
            if self.angle < 0:
                self.angle = 21.078791936
                self.moving_lr_vel = 0
            if self.state_collision:
                if self.vel_of_forward != -1:
                    left_animation()
            else:
                up_animation()
                left_animation()
        elif keys[settings.KEYS["MOVE UP"]] and keys[settings.KEYS["MOVE RIGHT"]]:
            if self.angle > 0:
                self.angle = -21.078791936
                self.moving_lr_vel = 0
            if self.state_collision:
                if self.vel_of_forward != -1:
                    right_animation()
            else:
                up_animation()
                right_animation()
        elif keys[settings.KEYS["MOVE UP"]]:
            if self.state_collision:
                if self.vel_of_forward == -1:
                    up_animation()
            else:
                up_animation()
            return_side_move()
        elif keys[settings.KEYS["MOVE LEFT"]]:
            if self.angle < 0:
                self.angle = 21.078791936
                self.moving_lr_vel = 0
            left_animation()
            soft_back_animation()
        elif keys[settings.KEYS["MOVE RIGHT"]]:
            if self.angle > 0:
                self.angle = -21.078791936
                self.moving_lr_vel = 0
            right_animation()
            soft_back_animation()
        elif keys[settings.KEYS["MOVE DOWN"]]:
            down_animation()
            return_side_move()
        else:
            soft_back_animation()
            return_side_move()

        '''test = pg.time.get_ticks()
        up_animation()
        if self.rect.y == 49:
            print(test - self.last_update)
            exit()'''

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
                    self.vel_of_forward = self.max_speed

                self.vel_of_forward = max(self.vel_of_forward - self.acceleration * 0.85, 0)
                self.rect.y += self.vel_of_forward

                if self.vel_of_forward < 1:
                    self.vel_of_forward += 1.5

                if self.rect.y + self.vel_of_forward > self.min_y or self.rect.y > self.min_y:
                    self.rect.y = self.min_y
                else:
                    self.vel_of_forward = max(self.vel_of_forward - 0.1, 0)
                    self.rect.y += self.vel_of_forward

                if self.rect.y == self.min_y:
                    self.vel_of_forward = -1
                    self.speed_is_max = False

            else:
                self.speed = max(self.speed - 0.1 * 0.5, 0)

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

    def rotate_arrow_of_speedometer(self, screen, image_path, pos, scale=1):
        image = pg.image.load(image_path).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        image = pg.transform.scale(image, (width * scale, height * scale))

        image_rect = image.get_rect(topleft=(pos[0] - image.get_width() / 2, pos[1] - image.get_height() / 2))
        offset_center_to_pivot = pg.math.Vector2(pos) - image_rect.center

        speed = self.speed * (30 / self.max_speed)

        if self.speed != 0:
            self.arrow_angle = (speed + (0 if self.speed < self.max_speed else self.vel_of_forward / 2.5)) * 6 - 15

        rotated_offset = offset_center_to_pivot.rotate(-self.arrow_angle)

        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        rotated_image = pg.transform.rotate(image, -self.arrow_angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

        screen.blit(rotated_image, (rotated_image_rect.x + 85, rotated_image_rect.y + 85))
