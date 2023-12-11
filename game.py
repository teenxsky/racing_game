import sprites
import datetime
from menu import *
from objects import *
from sprites import *


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, 16, 2, 4096)
        pg.init()
        pg.display.set_caption("00 Racing")
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
        self.keys = {"MOUSEBUTTONDOWN": False, "BACK": False}

        # MENU

        self.main_menu = MainMenu(self)
        self.sets_menu = SetsMenu(self)
        self.garage_menu = GarageMenu(self)
        self.music_menu = MusicMenu(self)

        # BUTTONS GAME

        button_sound = pg.mixer.Sound("audio/button_sound.mp3")
        self.close_button_game = Button(580, 360, "images/buttons/close_button_off.png", "images/buttons/close_button_on.png", button_sound, 0.25)
        self.back_button = Button(700, 360, "images/buttons/back_button_off.png", "images/buttons/back_button_on.png", button_sound, 0.25)

        # BACKGROUND

        bg_summer_1 = Background("images/backgrounds/summer_road_1.png")
        bg_summer_1.resize(1280, 720)
        bg_summer_2 = Background("images/backgrounds/summer_road_2.png")
        bg_summer_2.resize(1280, 720)
        self.bgs = [bg_summer_1, bg_summer_2]

        # CARS

        self.player_car = GIF(f'images/cars/player_car_{settings.car}/', scale=1.1).gif
        self.opp1 = GIF("images/cars/opp1/", scale=1.15).gif
        #self.opp2 = GIF("images/cars/opp2/", scale=1.15).gif

        self.crash = pg.image.load('images/crash.png')
        self.crash_rect = self.crash.get_rect()

    def game_loop(self):
        def add_sprites(car_imgs, sprite_group, type="Vehicle"):
            for frame in range(len(car_imgs)):
                if type == "Vehicle":
                    car = sprites.Vehicle(0, 0, car_imgs[frame].image)
                elif type == "PlayerVehicle":
                    car = sprites.PlayerVehicle(790, 590, car_imgs[frame].image)
                sprite_group.add(car)

        self.enemy_speed = 2
        self.main_speed = 0
        self.angle_of_main = 0
        self.lives = 3

        self.player_group = pg.sprite.Group()
        self.enemies_group = pg.sprite.Group()

        add_sprites(self.opp1, self.enemies_group)
        add_sprites(self.player_car, self.player_group, "PlayerVehicle")

        P1 = Player(self.player_group.sprites())
        E1 = Enemy(self.enemies_group.sprites(), self.enemy_speed, self.main_speed)

        bg_summer_0 = Background("images/backgrounds/summer_road_0.png")
        bg_summer_0.resize(1280, 720)
        bg_summer_0.set_bgs(self.bgs, (95, 100), 10)  # SETS FOR RANDOM BG

        blinks_counter = 0

        while self.playing:
            self.check_events()

            if self.game_state == "COLLISION":
                if blinks_counter == 0:
                    P1.collision(True)
                    self.main_speed = P1.get_const(speed=True)
                    E1.set_speed(enemy_speed=self.enemy_speed, main_speed=self.main_speed)
                    E1.render_enemies(False)

                blinks_counter += 1

                a = datetime.datetime.now()
                b = datetime.datetime.now()

                while (b - a).microseconds < 300000:
                    self.blit_screen()
                    self.main_speed = P1.get_const(speed=True)
                    E1.set_speed(enemy_speed=self.enemy_speed, main_speed=self.main_speed)
                    bg_summer_0.random_scroll(self.screen, self.main_speed)
                    P1.move(self.screen)
                    E1.move(self.screen)
                    b = datetime.datetime.now()

                a = datetime.datetime.now()
                b = datetime.datetime.now()

                while (b - a).microseconds < 300000:
                    self.blit_screen()
                    self.main_speed = P1.get_const(speed=True)
                    E1.set_speed(enemy_speed=self.enemy_speed, main_speed=self.main_speed)
                    bg_summer_0.random_scroll(self.screen, self.main_speed)
                    P1.move(self.screen)
                    E1.move(self.screen)
                    Player.blit_rotate_center(P1, self.screen)
                    b = datetime.datetime.now()

                if blinks_counter == 6:
                    blinks_counter = 0
                    self.game_state = "GAME"

                    P1.collision(False)
                    E1.render_enemies(True)
                    P1.move(self.screen)
                    E1.move(self.screen)

                    self.angle_of_main = 0

                    Player.blit_rotate_center(P1, self.screen)

            elif self.game_state == "PAUSED":
                bg_summer_0.random_scroll(self.screen, 0)

                P1.set_const(speed=0, angle=self.angle_of_main, update_rate=0)
                E1.set_speed(enemy_speed=0, main_speed=0)

                E1.move(self.screen)

                Player.blit_rotate_center(P1, self.screen)

                if self.close_button_game.draw(self.screen, False) and self.clicked:
                    self.playing = False
                    self.game_state = "GAME"
                if self.back_button.draw(self.screen, False) and self.clicked:
                    self.game_state = "GAME"

            else:
                if P1.get_const(speed=True) == 0:
                    P1.set_const(speed=self.main_speed, angle=self.angle_of_main, update_rate=100)
                self.main_speed = P1.get_const(speed=True)
                E1.set_speed(enemy_speed=self.enemy_speed, main_speed=self.main_speed)

                bg_summer_0.random_scroll(self.screen, self.main_speed)

                P1.move(self.screen)
                E1.move(self.screen)

                self.main_speed = P1.get_const(speed=True)

                Player.blit_rotate_center(P1, self.screen)

                self.angle_of_main = P1.get_const(angle=True)

                player_mask = P1.get_const(mask=True)
                player_rect_x = P1.get_const(x=True)
                player_rect_y = P1.get_const(y=True)

                enemy_mask = E1.get_const(mask=True)
                enemy_rect_x = E1.get_const(x=True)
                enemy_rect_y = E1.get_const(y=True)

                if player_mask.overlap(enemy_mask, (enemy_rect_x - player_rect_x, enemy_rect_y - player_rect_y)):
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_state = "GAME_OVER"
                        '''self.crash_rect.center = [self.player_group.sprites()[0].rect.center[0],
                                                  self.player_group.sprites()[0].rect.top]'''
                    else:
                        self.game_state = "COLLISION"

            self.blit_screen()

        pg.time.delay(500)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running, self.playing = False, False
            if event.type == pg.MOUSEBUTTONDOWN:
                self.clicked = True
            else:
                self.clicked = False
            if event.type == pg.KEYDOWN:
                if event.key == settings.KEYS["MOVE BACK"]:
                    if self.game_state == "PAUSED":
                        self.game_state = "GAME"
                    else:
                        self.game_state = "PAUSED"

    def blit_screen(self):
        for button in self.keys.keys():
            self.keys[button] = False
        self.window.blit(self.screen, (0, 0))
        pg.display.update()
        self.frame_per_second.tick(self.FPS)

    def draw_text(self, x, y, text, size=30):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
