from menu import *
from objects import *
from sprites import *


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, 16, 2, 4096)
        pg.init()
        pg.display.set_caption("00 Racing")
        icon = pg.image.load("images/icon.png")
        pg.display.set_icon(icon)
        self.running, self.playing = True, False
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 720
        self.window = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen = pg.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.FPS = 60
        self.font_name = "fonts/pxl_tactical.ttf"
        self.frame_per_second = pg.time.Clock()
        pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_HAND))

        # HANDLE_EVENTS

        self.clicked = False
        self.menu_state = "MENU"
        self.game_state = "GAME"
        self.keys = {"MOUSE DOWN": False, "BACK": False, "ENTER": False,
                     "MOVE UP": False, "MOVE DOWN": False, "MOUSEWHEEL": 0,
                     "MOVE RIGHT": False, "MOVE LEFT": False
                     }

        # MENU

        self.main_menu = MainMenu(self)
        self.sets_menu = SetsMenu(self)
        self.garage_menu = GarageMenu(self)
        self.music_menu = MusicMenu(self)
        self.authors_menu = Authors(self)

        # BUTTONS GAME

        button_sound = pg.mixer.Sound("audio/button_sound.mp3")
        self.close_button_game = Button(580, 360, "images/buttons/close_button_off.png",
                                        "images/buttons/close_button_on.png", button_sound, 0.25)
        self.back_button = Button(700, 360, "images/buttons/back_button_off.png", "images/buttons/back_button_on.png",
                                  button_sound, 0.25)

        # BACKGROUND

        self.curr_level = 0

        # HINTS

        self.forward_hint = GIF("images/HUD/controls/forward/", scale=0.15)
        self.left_hint = GIF("images/HUD/controls/left/", scale=0.15)
        self.right_hint = GIF("images/HUD/controls/right/", scale=0.15)

        # CARS

        self.opp1 = GIF("images/cars/opps/opp1/", scale=0.75).gif
        self.opp2 = GIF("images/cars/opps/opp2/", scale=0.7).gif
        self.opp3 = GIF("images/cars/opps/opp3/", scale=0.75).gif
        self.opp4 = GIF("images/cars/opps/opp4/", scale=0.65).gif

        self.first_enemy = None
        self.second_enemy = None
        self.third_enemy = None

        gold_coin_image = pg.image.load("images/HUD/coins/MonedaD.png").convert_alpha()
        self.gold_coin_images = get_sheets(gold_coin_image, 5, 3)

        rubin_coin_image = pg.image.load("images/HUD/coins/spr_coin_roj.png").convert_alpha()
        self.rubin_coin_images = get_sheets(rubin_coin_image, 4, 3)

        self.oil_stain_image = Picture(0, 0, "images/HUD/oil_stain.png")

        self.speedometer_base = Picture(1090, 530, "images/HUD/speedometer/base.png", 1.35)

        # MUSIC

        self.player = MusicPlayer("audio/music/")
        self.player.set_volume()
        # self.player.play()
    def actions_with_enemies(self, type_of_actions):
        if type_of_actions == "move":
            current_time = pg.time.get_ticks()
            if self.map_number == 1:
                self.enemies[self.first_enemy].move(self.screen)

                if self.enemies[self.first_enemy].get_const(y=True) == -300:
                    self.score += 1
                    self.first_enemy = (self.first_enemy + 1) % 4

            if self.map_number == 2:
                for i in range(4):
                    if i != self.first_enemy:
                        self.enemies[self.first_enemy].set_speed(
                            another_x=self.enemies[i].get_const(x=True))

                for i in range(4):
                    if i != self.second_enemy:
                        self.enemies[self.second_enemy].set_speed(
                            another_x=self.enemies[i].get_const(x=True))

                self.enemies[self.first_enemy].set_speed(rendering_frequency=-1)
                self.enemies[self.first_enemy].move(self.screen)

                self.enemies[self.second_enemy].set_speed(rendering_frequency=1000)
                self.enemies[self.second_enemy].move(self.screen)

                if self.enemies[self.first_enemy].get_const(y=True) == -300:
                    self.score += 1
                    self.first_enemy = (self.first_enemy + 2) % 4

                if self.enemies[self.second_enemy].get_const(y=True) == -300:
                    if current_time - self.time2 > 1200:
                        self.score += 1
                    self.second_enemy = (self.second_enemy + 2) % 4

            if self.map_number == 3:
                for i in range(4):
                    if i != self.first_enemy:
                        self.enemies[self.first_enemy].set_speed(
                            another_x=self.enemies[i].get_const(x=True))

                for i in range(4):
                    if i != self.second_enemy:
                        self.enemies[self.second_enemy].set_speed(
                            another_x=self.enemies[i].get_const(x=True))

                for i in range(4):
                    if i != self.third_enemy:
                        self.enemies[self.third_enemy].set_speed(
                            another_x=self.enemies[i].get_const(x=True))

                self.enemies[self.first_enemy].set_speed(rendering_frequency=-1)
                self.enemies[self.first_enemy].move(self.screen)

                self.enemies[self.second_enemy].set_speed(rendering_frequency=1000)
                self.enemies[self.second_enemy].move(self.screen)

                self.enemies[self.third_enemy].set_speed(rendering_frequency=2000)
                self.enemies[self.third_enemy].move(self.screen)

                if self.enemies[self.first_enemy].get_const(y=True) == -300:
                    self.score += 1
                    for i in range(self.first_enemy + 1, 4 + self.first_enemy):
                        if self.enemies[i % 4].get_const(y=True) == -300:
                            self.first_enemy = i % 4
                            break

                if self.enemies[self.second_enemy].get_const(y=True) == -300:
                    if current_time - self.time2 > 1200:
                        self.score += 1
                    for i in range(self.second_enemy + 1, 4 + self.second_enemy):
                        if self.enemies[i % 4].get_const(y=True) == -300:
                            self.second_enemy = i % 4
                            break

                if self.enemies[self.third_enemy].get_const(y=True) == -300:
                    if current_time - self.time2 > 2200:
                        self.score += 1
                    for i in range(self.third_enemy + 1, 4 + self.third_enemy):
                        if self.enemies[i % 4].get_const(y=True) == -300:
                            self.third_enemy = i % 4
                            break

        if type_of_actions == "stop":
            for obj in self.enemies:
                obj.set_speed(enemy_speed=0, main_speed=0)

        if type_of_actions == "set_speed":
            for obj in self.enemies:
                obj.set_speed(enemy_speed=self.enemy_speed, main_speed=self.main_speed)

    def collision_with_enemies(self, enemy):
        player_mask = self.P1.get_const(mask=True)
        player_rect_x = self.P1.get_const(x=True)
        player_rect_y = self.P1.get_const(y=True)

        enemy_mask = enemy.get_const(mask=True)
        enemy_rect_x = enemy.get_const(x=True)
        enemy_rect_y = enemy.get_const(y=True)

        if enemy_mask is not None:
            if player_mask.overlap(enemy_mask, (enemy_rect_x - player_rect_x, enemy_rect_y - player_rect_y)):
                self.lives -= 1
                if self.lives == 0:
                    self.game_state = "GAME_OVER"

                    pos = [self.player_group.sprites()[0].rect.center[0], self.player_group.sprites()[0].rect.top]
                    explosion = Explosion(pos[0], pos[1])
                    self.explosion_group.add(explosion)

                else:
                    self.game_state = "COLLISION"

    def game_over(self):
        self.lives = 3
        self.first_bg.random_scroll(self.screen, 0)

        #остановка игры, после которой пиши уже геймовер

        self.P1.set_const(speed=0, angle=self.angle_of_main, update_rate=0)
        self.actions_with_enemies("stop")
        self.actions_with_enemies("move")

        self.Gold_Co.set_const(speed=0)
        self.Gold_Co.move(self.screen)
        self.Ruby_Co.set_const(speed=0)
        self.Ruby_Co.move(self.screen)
        self.Oil.set_const(speed=0)
        self.Oil.move(self.screen)

        Player.blit_rotate_center(self.P1, self.screen)

        self.screen.blit(self.speedometer_base.image, self.speedometer_base.center)
        self.P1.rotate_arrow_of_speedometer(self.screen, "images/HUD/speedometer/arrow.png",
                                            self.speedometer_base.center, 1.35)

        self.explosion_group.draw(self.screen)
        self.explosion_group.update()

        # остановка игры

        if self.close_button_game.draw(self.screen, False) and self.clicked:
            self.playing = False
            self.game_state = "GAME"
        if self.back_button.draw(self.screen, False) and self.clicked:
            self.game_state = "GAME"

    def paused(self):
        self.first_bg.random_scroll(self.screen, 0)
        self.time = pg.time.get_ticks()

        self.P1.set_const(speed=0, angle=self.angle_of_main, update_rate=0)
        self.actions_with_enemies("stop")
        self.actions_with_enemies("move")

        self.Gold_Co.set_const(speed=0)
        self.Gold_Co.move(self.screen)
        self.Ruby_Co.set_const(speed=0)
        self.Ruby_Co.move(self.screen)
        self.Oil.set_const(speed=0)
        self.Oil.move(self.screen)

        Player.blit_rotate_center(self.P1, self.screen)

        self.screen.blit(self.speedometer_base.image, self.speedometer_base.center)
        self.P1.rotate_arrow_of_speedometer(self.screen, "images/HUD/speedometer/arrow.png",
                                            self.speedometer_base.center, 1.35)

        if self.close_button_game.draw(self.screen, False) and self.clicked:
            self.playing = False
            if self.blinks_counter != 0:
                self.game_state = "COLLISION"
            else:
                self.game_state = "GAME"
        if self.back_button.draw(self.screen, False) and self.clicked:
            if self.blinks_counter != 0:
                self.game_state = "COLLISION"
            else:
                self.game_state = "GAME"

    def collision(self):
        if self.blinks_counter == 0:
            self.P1.collision(True)
            self.E1.render(False)
            self.Gold_Co.render(False)
            self.Ruby_Co.render(False)
            self.Oil.render(False)

        self.blinks_counter += 1

        self.P1.set_const(speed=self.main_speed)

        a = datetime.datetime.now()
        b = datetime.datetime.now()

        while (b - a).microseconds < 250000:
            self.blit_screen()
            self.main_speed = self.P1.get_const(speed=True)
            self.actions_with_enemies("set_speed")
            self.first_bg.random_scroll(self.screen, self.main_speed)
            self.hud()
            self.P1.move(self.screen)
            self.actions_with_enemies("move")
            b = datetime.datetime.now()
            self.screen.blit(self.speedometer_base.image, self.speedometer_base.center)
            self.P1.rotate_arrow_of_speedometer(self.screen, "images/HUD/speedometer/arrow.png",
                                                self.speedometer_base.center, 1.35)

            self.Gold_Co.set_const(speed=self.main_speed)
            self.Ruby_Co.set_const(speed=self.main_speed)
            self.Oil.set_const(speed=self.main_speed)

            self.Oil.move(self.screen)

            oil_mask = self.Oil.get_const(mask=True)
            oil_rect_x = self.Oil.get_const(x=True)
            oil_rect_y = self.Oil.get_const(y=True)

            player_mask = self.P1.get_const(mask=True)
            player_rect_x = self.P1.get_const(x=True)
            player_rect_y = self.P1.get_const(y=True)

            self.Gold_Co.move(self.screen)

            gold_coin_mask = self.Gold_Co.get_const(mask=True)
            gold_coin_rect_x = self.Gold_Co.get_const(x=True)
            gold_coin_rect_y = self.Gold_Co.get_const(y=True)

            self.Ruby_Co.move(self.screen)

            rubin_coin_mask = self.Ruby_Co.get_const(mask=True)
            rubin_coin_rect_x = self.Ruby_Co.get_const(x=True)
            rubin_coin_rect_y = self.Ruby_Co.get_const(y=True)

            if oil_mask is not None:
                if player_mask.overlap(oil_mask, (oil_rect_x - player_rect_x, oil_rect_y - player_rect_y)):
                    if self.P1.get_const(vel_of_forward=True) != -1:
                        self.P1.collision(True)
                    else:
                        self.P1.collision(False)

                    if self.main_speed > 5:
                        self.main_speed /= 1.05

                    self.P1.set_const(speed=self.main_speed, angle=self.angle_of_main, update_rate=100)
                    self.actions_with_enemies("set_speed")

            if player_mask.overlap(gold_coin_mask,
                                   (gold_coin_rect_x - player_rect_x, gold_coin_rect_y - player_rect_y)):
                self.Gold_Co = CoinsMechanics(self.coins_group.sprites(), self.main_speed, "gold")
                self.coins += 1

            if rubin_coin_mask is not None:
                if player_mask.overlap(rubin_coin_mask,
                                       (rubin_coin_rect_x - player_rect_x, rubin_coin_rect_y - player_rect_y)):
                    self.Ruby_Co = CoinsMechanics(self.ruby_group.sprites(), self.main_speed, "ruby")
                    self.coins += 10

        a = datetime.datetime.now()
        b = datetime.datetime.now()

        while (b - a).microseconds < 250000:
            self.blit_screen()
            self.main_speed = self.P1.get_const(speed=True)
            self.actions_with_enemies("set_speed")
            self.first_bg.random_scroll(self.screen, self.main_speed)
            self.hud()
            self.P1.move(self.screen)
            self.actions_with_enemies("move")
            Player.blit_rotate_center(self.P1, self.screen)
            b = datetime.datetime.now()
            self.screen.blit(self.speedometer_base.image, self.speedometer_base.center)
            self.P1.rotate_arrow_of_speedometer(self.screen, "images/HUD/speedometer/arrow.png",
                                                self.speedometer_base.center, 1.35)

            self.Gold_Co.set_const(speed=self.main_speed)
            self.Ruby_Co.set_const(speed=self.main_speed)
            self.Oil.set_const(speed=self.main_speed)

            self.Oil.move(self.screen)

            oil_mask = self.Oil.get_const(mask=True)
            oil_rect_x = self.Oil.get_const(x=True)
            oil_rect_y = self.Oil.get_const(y=True)

            player_mask = self.P1.get_const(mask=True)
            player_rect_x = self.P1.get_const(x=True)
            player_rect_y = self.P1.get_const(y=True)

            self.Gold_Co.move(self.screen)

            gold_coin_mask = self.Gold_Co.get_const(mask=True)
            gold_coin_rect_x = self.Gold_Co.get_const(x=True)
            gold_coin_rect_y = self.Gold_Co.get_const(y=True)

            self.Ruby_Co.move(self.screen)

            rubin_coin_mask = self.Ruby_Co.get_const(mask=True)
            rubin_coin_rect_x = self.Ruby_Co.get_const(x=True)
            rubin_coin_rect_y = self.Ruby_Co.get_const(y=True)

            if oil_mask is not None:
                if player_mask.overlap(oil_mask, (oil_rect_x - player_rect_x, oil_rect_y - player_rect_y)):
                    if self.P1.get_const(vel_of_forward=True) != -1:
                        self.P1.collision(True)
                    else:
                        self.P1.collision(False)

                    if self.main_speed > 5:
                        self.main_speed /= 1.05

                    self.P1.set_const(speed=self.main_speed, angle=self.angle_of_main, update_rate=100)
                    self.actions_with_enemies("set_speed")

            if player_mask.overlap(gold_coin_mask,
                                   (gold_coin_rect_x - player_rect_x, gold_coin_rect_y - player_rect_y)):
                self.Gold_Co = CoinsMechanics(self.coins_group.sprites(), self.main_speed, "gold")
                self.coins += 1

            if rubin_coin_mask is not None:
                if player_mask.overlap(rubin_coin_mask,
                                       (rubin_coin_rect_x - player_rect_x, rubin_coin_rect_y - player_rect_y)):
                    self.Ruby_Co = CoinsMechanics(self.ruby_group.sprites(), self.main_speed, "ruby")
                    self.coins += 10

        if self.blinks_counter == 3:
            self.blinks_counter = 0
            self.game_state = "GAME"

            self.P1.collision(False)
            self.E1.render(True)
            self.Gold_Co.render(True)
            self.Ruby_Co.render(True)
            self.Oil.render(True)
            self.P1.move(self.screen)
            self.actions_with_enemies("move")

            self.angle_of_main = 0

            Player.blit_rotate_center(self.P1, self.screen)

    def game(self):
        if self.P1.get_const(speed=True) == 0:
            self.P1.set_const(speed=self.main_speed, angle=self.angle_of_main, update_rate=100)
        self.main_speed = self.P1.get_const(speed=True)
        self.actions_with_enemies("set_speed")
        self.Gold_Co.set_const(speed=self.main_speed)
        self.Ruby_Co.set_const(speed=self.main_speed)
        self.Oil.set_const(speed=self.main_speed)

        self.first_bg.random_scroll(self.screen, self.main_speed)

        self.P1.move(self.screen)
        self.actions_with_enemies("move")

        self.main_speed = self.P1.get_const(speed=True)
        Player.blit_rotate_center(self.P1, self.screen)
        self.angle_of_main = self.P1.get_const(angle=True)

        self.Oil.move(self.screen)

        oil_mask = self.Oil.get_const(mask=True)
        oil_rect_x = self.Oil.get_const(x=True)
        oil_rect_y = self.Oil.get_const(y=True)

        player_mask = self.P1.get_const(mask=True)
        player_rect_x = self.P1.get_const(x=True)
        player_rect_y = self.P1.get_const(y=True)

        self.Gold_Co.move(self.screen)

        gold_coin_mask = self.Gold_Co.get_const(mask=True)
        gold_coin_rect_x = self.Gold_Co.get_const(x=True)
        gold_coin_rect_y = self.Gold_Co.get_const(y=True)

        self.Ruby_Co.move(self.screen)

        rubin_coin_mask = self.Ruby_Co.get_const(mask=True)
        rubin_coin_rect_x = self.Ruby_Co.get_const(x=True)
        rubin_coin_rect_y = self.Ruby_Co.get_const(y=True)

        if oil_mask is not None:
            if player_mask.overlap(oil_mask, (oil_rect_x - player_rect_x, oil_rect_y - player_rect_y)):
                if self.P1.get_const(vel_of_forward=True) != -1:
                    self.P1.collision(True)
                else:
                    self.P1.collision(False)

                if self.main_speed > 5:
                    self.main_speed /= 1.05

                self.P1.set_const(speed=self.main_speed, angle=self.angle_of_main, update_rate=100)
                self.actions_with_enemies("set_speed")

        if player_mask.overlap(gold_coin_mask,
                               (gold_coin_rect_x - player_rect_x, gold_coin_rect_y - player_rect_y)):
            self.Gold_Co = CoinsMechanics(self.coins_group.sprites(), self.main_speed, "gold")
            self.coins += 1

        if rubin_coin_mask is not None:
            if player_mask.overlap(rubin_coin_mask,
                                   (rubin_coin_rect_x - player_rect_x, rubin_coin_rect_y - player_rect_y)):
                self.Ruby_Co = CoinsMechanics(self.ruby_group.sprites(), self.main_speed, "ruby")
                self.coins += 10

        self.collision_with_enemies(self.E1)
        self.collision_with_enemies(self.E2)
        self.collision_with_enemies(self.E3)
        self.collision_with_enemies(self.E4)

        if all(not i for i in pg.key.get_pressed()):
            if pg.time.get_ticks() - self.time > 5000:
                self.show_hints()
        else:
            self.time = pg.time.get_ticks()

    def hud(self):
        color = None
        if self.map_number == 1:
            color = (255, 255, 255)
        if self.map_number == 2:
            color = (0, 0, 0)

        Text(105, 23, "COINS:" + str(self.coins), scale=35, color=color).draw(self.screen)
        Text(105, 63, "SCORE:" + str(self.score), scale=35, color=color).draw(self.screen)

        self.screen.blit(self.speedometer_base.image, self.speedometer_base.center)
        self.P1.rotate_arrow_of_speedometer(self.screen, "images/HUD/speedometer/arrow.png",
                                            self.speedometer_base.center, 1.35)

        self.player.draw_current_song(self.screen, (10, 710), set_bottomleft=True)

    def game_loop(self):
        def add_sprites(imgs, sprite_group, type=None):
            obj = None
            for frame in range(len(imgs)):
                if type == "Vehicle":
                    obj = OppVehicle(0, 0, imgs[frame].image)
                if type == "PlayerVehicle":
                    obj = PlayerVehicle(790, 590, imgs[frame].image)
                if type == "Elements":
                    obj = Elements(0, 0, imgs[frame])

                sprite_group.add(obj)

        def choose_car():
            i = 0
            player_car = settings.cars[i]
            while not settings.cars[i]["chosen"]:
                i += 1
                player_car = settings.cars[i]
            return player_car

        self.map_number = int(settings.levels[self.curr_level]["number"])

        self.lives = 3
        self.blinks_counter = 0
        self.coins = 0
        self.score = 0

        self.main_speed = 0
        max_player_speed = choose_car()["specs"]["speed"]
        player_acceleration = choose_car()["specs"]["braking"]
        change_moving_lr_vel = choose_car()["specs"]["driveability"]

        self.enemy_speed = 2
        self.angle_of_main = 0

        self.player_group = pg.sprite.Group()
        enemy1_group = pg.sprite.Group()
        enemy2_group = pg.sprite.Group()
        enemy3_group = pg.sprite.Group()
        enemy4_group = pg.sprite.Group()

        self.coins_group = pg.sprite.Group()
        self.ruby_group = pg.sprite.Group()
        oil_group = pg.sprite.Group()
        self.explosion_group = pg.sprite.Group()

        add_sprites(GIF(f'images/cars/{choose_car()["name"]} topdown/', scale=0.4).gif, self.player_group, "PlayerVehicle")
        add_sprites(self.opp1, enemy1_group, "Vehicle")
        add_sprites(self.opp2, enemy2_group, "Vehicle")
        add_sprites(self.opp3, enemy3_group, "Vehicle")
        add_sprites(self.opp4, enemy4_group, "Vehicle")

        add_sprites(self.gold_coin_images, self.coins_group, "Elements")
        add_sprites(self.rubin_coin_images, self.ruby_group, "Elements")
        add_sprites([self.oil_stain_image.image], oil_group, "Elements")

        self.P1 = Player(self.player_group.sprites(), max_player_speed, player_acceleration, change_moving_lr_vel)

        self.E1 = Enemy(enemy1_group.sprites(), self.enemy_speed, self.main_speed)
        self.E2 = Enemy(enemy2_group.sprites(), self.enemy_speed, self.main_speed)
        self.E3 = Enemy(enemy3_group.sprites(), self.enemy_speed, self.main_speed)
        self.E4 = Enemy(enemy4_group.sprites(), self.enemy_speed, self.main_speed)

        self.enemies = [self.E1, self.E2, self.E3, self.E4]
        self.first_enemy = 0
        self.second_enemy = 1
        self.third_enemy = 2

        self.Gold_Co = CoinsMechanics(self.coins_group.sprites(), self.main_speed, "gold")
        self.Ruby_Co = CoinsMechanics(self.ruby_group.sprites(), self.main_speed, "ruby")
        self.Oil = OilMechanics(oil_group.sprites(), self.main_speed)

        self.first_bg = None
        bgs = []
        for file in sorted(os.listdir(f'images/backgrounds/levels/level{str(self.map_number)}/')):
            if ".png" in file:
                bg = Background(f'images/backgrounds/levels/level{str(self.map_number)}/' + file)
                bg.resize(1280, 720)
                if self.first_bg:
                    bgs.append(bg)
                else:
                    self.first_bg = bg
        self.first_bg.set_bgs(bgs, (60, 5, 20, 30, 5), 10)

        self.time = pg.time.get_ticks()
        self.time2 = pg.time.get_ticks()

        while self.playing:
            self.check_events()

            if self.game_state == "GAME_OVER":
                self.game_over()

            elif self.game_state == "PAUSED":
                self.paused()

            elif self.game_state == "COLLISION":
                self.collision()

            elif self.game_state == "GAME":
                self.game()

            self.hud()

            self.blit_screen()

        pg.time.delay(500)

    def show_hints(self):
        bar = pg.surface.Surface((270, 100), pg.SRCALPHA).convert_alpha()
        bar_rect = bar.get_rect()
        bar_rect.center = (640, 360)

        bar.fill((0, 0, 0, 255))

        self.forward_hint.draw(bar, coordinates=(bar.get_width() / 2, bar.get_height() / 2 - 10))
        move_up = Text(0, 0, pg.key.name(settings.KEYS["MOVE UP"]), scale=15)
        move_up.rect.center = (bar.get_width() / 2, bar.get_height() / 2 + 30)
        move_up.draw(bar)

        self.left_hint.draw(bar, coordinates=(bar.get_width() / 2 - 100, bar.get_height() / 2 - 10))
        move_left = Text(0, 0, pg.key.name(settings.KEYS["MOVE LEFT"]), scale=15)
        move_left.rect.center = (bar.get_width() / 2 - 100, bar.get_height() / 2 + 30)
        move_left.draw(bar)

        self.right_hint.draw(bar, coordinates=(bar.get_width() / 2 + 100, bar.get_height() / 2 - 10))
        move_right = Text(0, 0, pg.key.name(settings.KEYS["MOVE RIGHT"]), scale=15)
        move_right.rect.center = (bar.get_width() / 2 + 100, bar.get_height() / 2 + 30)
        move_right.draw(bar)

        self.screen.blit(bar, bar_rect)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running, self.playing = False, False
            if event.type == pg.MOUSEBUTTONDOWN:
                self.clicked = True
            else:
                self.clicked = False
            if event.type == pg.KEYDOWN:
                if event.key == settings.KEYS["BACK"]:
                    self.keys["BACK"] = True
                    if self.game_state == "PAUSED":
                        self.game_state = "GAME"
                    else:
                        self.game_state = "PAUSED"
                if event.key == settings.KEYS["ENTER"]:
                    self.keys["ENTER"] = True
                if event.key == settings.KEYS["PLAY MUSIC"]:
                    self.player.play()
                if event.key == settings.KEYS["CHANGE MUSIC"]:
                    self.player.next()
            if event.type == self.player.MUSIC_END:
                self.player.playing = False
                if self.player.loop:
                    self.player.play()
                else:
                    self.player.next()

    def blit_screen(self):
        for button in self.keys.keys():
            self.keys[button] = 0
        self.window.blit(self.screen, (0, 0))
        pg.display.update()
        self.frame_per_second.tick(self.FPS)