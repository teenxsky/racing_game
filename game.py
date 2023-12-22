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

        self.opp1 = GIF("images/cars/opp1/", scale=0.7).gif
        # self.opp2 = GIF("images/cars/opp2/", scale=1.15).gif

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

        def chose_car():
            i = 0
            player_car = GIF(f'images/cars/{settings.cars[i]["name"]}_topdown/', scale=0.7).gif
            while not settings.cars[i]["chosen"]:
                i += 1
                player_car = GIF(f'images/cars/{settings.cars[i]["name"]}_topdown/', scale=0.7).gif
            return player_car

        lives = 3
        self.blinks_counter = 0
        self.coins = 0
        self.score = 0

        main_speed = 0
        max_player_speed = 12
        player_acceleration = 0.1
        change_moving_lr_vel = 0.5

        enemy_speed = 2
        angle_of_main = 0
        coins_speed = 5

        player_group = pg.sprite.Group()
        enemies_group = pg.sprite.Group()
        coins_group = pg.sprite.Group()
        ruby_group = pg.sprite.Group()
        oil_group = pg.sprite.Group()
        explosion_group = pg.sprite.Group()

        add_sprites(chose_car(), player_group, "PlayerVehicle")
        add_sprites(self.opp1, enemies_group, "Vehicle")
        add_sprites(self.gold_coin_images, coins_group, "Elements")
        add_sprites(self.rubin_coin_images, ruby_group, "Elements")
        add_sprites([self.oil_stain_image.image], oil_group, "Elements")

        P1 = Player(player_group.sprites(), max_player_speed, player_acceleration, change_moving_lr_vel)
        '''P1.set_const(speed=max_player_speed, y=49, vel_of_forward=10)'''

        E1 = Enemy(enemies_group.sprites(), enemy_speed, main_speed)
        Gold_Co = CoinsMechanics(coins_group.sprites(), coins_speed, "gold")
        Ruby_Co = CoinsMechanics(ruby_group.sprites(), coins_speed * 2, "ruby")
        Oil = OilMechanics(oil_group.sprites(), main_speed)

        first_bg = None
        bgs = []
        for file in sorted(os.listdir(f'images/backgrounds/levels/level{settings.levels[self.curr_level]["number"]}/')):
            if ".png" in file:
                bg = Background(f'images/backgrounds/levels/level{settings.levels[self.curr_level]["number"]}/' + file)
                bg.resize(1280, 720)
                if first_bg:
                    bgs.append(bg)
                else:
                    first_bg = bg
        first_bg.set_bgs(bgs, (60, 5, 20, 30, 5), 10)

        time = pg.time.get_ticks()

        while self.playing:
            self.check_events()

            if self.game_state == "GAME_OVER":  # сделал временную копию условия паузы, для геймовера, переделай потом под экран геймовера
                lives = 3
                first_bg.random_scroll(self.screen, 0)

                P1.set_const(speed=0, angle=angle_of_main, update_rate=0)
                E1.set_speed(enemy_speed=0, main_speed=0)
                E1.move(self.screen)

                Gold_Co.set_const(speed=0)
                Gold_Co.move(self.screen)
                Ruby_Co.set_const(speed=0)
                Ruby_Co.move(self.screen)
                Oil.set_const(speed=0)
                Oil.move(self.screen)

                Player.blit_rotate_center(P1, self.screen)

                self.screen.blit(self.speedometer_base.image, self.speedometer_base.center)
                P1.rotate_arrow_of_speedometer(self.screen, "images/HUD/speedometer/arrow.png",
                                               self.speedometer_base.center, 1.35)

                if self.close_button_game.draw(self.screen, False) and self.clicked:
                    self.playing = False
                    self.game_state = "GAME"
                if self.back_button.draw(self.screen, False) and self.clicked:
                    self.game_state = "GAME"

                explosion_group.draw(self.screen)
                explosion_group.update()

            elif self.game_state == "PAUSED":
                first_bg.random_scroll(self.screen, 0)
                time = pg.time.get_ticks()

                P1.set_const(speed=0, angle=angle_of_main, update_rate=0)
                E1.set_speed(enemy_speed=0, main_speed=0)
                E1.move(self.screen)

                Gold_Co.set_const(speed=0)
                Gold_Co.move(self.screen)
                Ruby_Co.set_const(speed=0)
                Ruby_Co.move(self.screen)
                Oil.set_const(speed=0)
                Oil.move(self.screen)

                Player.blit_rotate_center(P1, self.screen)

                self.screen.blit(self.speedometer_base.image, self.speedometer_base.center)
                P1.rotate_arrow_of_speedometer(self.screen, "images/HUD/speedometer/arrow.png",
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

            elif self.game_state == "COLLISION":
                if self.blinks_counter == 0:
                    P1.collision(True)
                    E1.set_speed(enemy_speed=enemy_speed, main_speed=0)
                    E1.render(False)
                    Gold_Co.render(False)
                    Ruby_Co.render(False)
                    Oil.render(False)

                self.blinks_counter += 1

                P1.set_const(speed=main_speed)

                a = datetime.datetime.now()
                b = datetime.datetime.now()

                while (b - a).microseconds < 300000:
                    self.blit_screen()
                    main_speed = P1.get_const(speed=True)
                    E1.set_speed(enemy_speed=enemy_speed, main_speed=main_speed)
                    first_bg.random_scroll(self.screen, main_speed)
                    P1.move(self.screen)
                    E1.move(self.screen)
                    b = datetime.datetime.now()
                    self.screen.blit(self.speedometer_base.image, self.speedometer_base.center)
                    P1.rotate_arrow_of_speedometer(self.screen, "images/HUD/speedometer/arrow.png",
                                                   self.speedometer_base.center, 1.35)

                a = datetime.datetime.now()
                b = datetime.datetime.now()

                while (b - a).microseconds < 300000:
                    self.blit_screen()
                    main_speed = P1.get_const(speed=True)
                    E1.set_speed(enemy_speed=enemy_speed, main_speed=main_speed)
                    first_bg.random_scroll(self.screen, main_speed)
                    P1.move(self.screen)
                    E1.move(self.screen)
                    Player.blit_rotate_center(P1, self.screen)
                    b = datetime.datetime.now()
                    self.screen.blit(self.speedometer_base.image, self.speedometer_base.center)
                    P1.rotate_arrow_of_speedometer(self.screen, "images/HUD/speedometer/arrow.png",
                                                   self.speedometer_base.center, 1.35)

                if self.blinks_counter == 3:
                    self.blinks_counter = 0
                    self.game_state = "GAME"

                    P1.collision(False)
                    E1.render(True)
                    Gold_Co.render(True)
                    Ruby_Co.render(True)
                    Oil.render(True)
                    P1.move(self.screen)
                    E1.move(self.screen)

                    angle_of_main = 0

                    Player.blit_rotate_center(P1, self.screen)

            elif self.game_state == "GAME":
                if P1.get_const(speed=True) == 0:
                    P1.set_const(speed=main_speed, angle=angle_of_main, update_rate=100)
                main_speed = P1.get_const(speed=True)
                E1.set_speed(enemy_speed=enemy_speed, main_speed=main_speed)
                Gold_Co.set_const(speed=coins_speed)
                Ruby_Co.set_const(speed=coins_speed)
                Oil.set_const(speed=main_speed)

                first_bg.random_scroll(self.screen, main_speed)

                Oil.move(self.screen)

                oil_mask = Oil.get_const(mask=True)
                oil_rect_x = Oil.get_const(x=True)
                oil_rect_y = Oil.get_const(y=True)

                P1.move(self.screen)
                E1.move(self.screen)

                main_speed = P1.get_const(speed=True)
                Player.blit_rotate_center(P1, self.screen)
                angle_of_main = P1.get_const(angle=True)

                player_mask = P1.get_const(mask=True)
                player_rect_x = P1.get_const(x=True)
                player_rect_y = P1.get_const(y=True)

                enemy_mask = E1.get_const(mask=True)
                enemy_rect_x = E1.get_const(x=True)
                enemy_rect_y = E1.get_const(y=True)

                Gold_Co.move(self.screen)

                gold_coin_mask = Gold_Co.get_const(mask=True)
                gold_coin_rect_x = Gold_Co.get_const(x=True)
                gold_coin_rect_y = Gold_Co.get_const(y=True)

                Ruby_Co.move(self.screen)

                rubin_coin_mask = Ruby_Co.get_const(mask=True)
                rubin_coin_rect_x = Ruby_Co.get_const(x=True)
                rubin_coin_rect_y = Ruby_Co.get_const(y=True)

                if enemy_rect_y == -300:
                    self.score += 1

                if oil_mask is not None:
                    if player_mask.overlap(oil_mask, (oil_rect_x - player_rect_x, oil_rect_y - player_rect_y)):
                        if P1.get_const(vel_of_forward=True) != -1:
                            P1.collision(True)
                        else:
                            P1.collision(False)

                        if main_speed > 5:
                            main_speed /= 1.05

                        P1.set_const(speed=main_speed, angle=angle_of_main, update_rate=100)
                        E1.set_speed(enemy_speed=enemy_speed, main_speed=main_speed)

                if player_mask.overlap(enemy_mask, (enemy_rect_x - player_rect_x, enemy_rect_y - player_rect_y)):
                    lives -= 1
                    if lives == 0:
                        self.game_state = "GAME_OVER"

                        pos = [player_group.sprites()[0].rect.center[0], player_group.sprites()[0].rect.top]
                        explosion = Explosion(pos[0], pos[1])
                        explosion_group.add(explosion)

                    else:
                        self.game_state = "COLLISION"

                if player_mask.overlap(gold_coin_mask,
                                       (gold_coin_rect_x - player_rect_x, gold_coin_rect_y - player_rect_y)):
                    Gold_Co = CoinsMechanics(coins_group.sprites(), coins_speed, "gold")
                    self.coins += 1

                if rubin_coin_mask is not None:
                    if player_mask.overlap(rubin_coin_mask,
                                           (rubin_coin_rect_x - player_rect_x, rubin_coin_rect_y - player_rect_y)):
                        Ruby_Co = CoinsMechanics(ruby_group.sprites(), coins_speed * 2, "ruby")
                        self.coins += 10

                if all(not i for i in pg.key.get_pressed()):
                    if pg.time.get_ticks() - time > 5000:
                        self.show_hints()
                else:
                    time = pg.time.get_ticks()

            self.screen.blit(self.speedometer_base.image, self.speedometer_base.center)
            P1.rotate_arrow_of_speedometer(self.screen, "images/HUD/speedometer/arrow.png",
                                           self.speedometer_base.center, 1.35)

            self.player.draw_current_song(self.screen, (10, 710), set_bottomleft=True)

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
