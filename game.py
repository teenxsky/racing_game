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
        self.keys = {"MOUSEBUTTONDOWN": False,
                     "K_ESCAPE": False}
        # MENU

        self.main_menu = MainMenu(self)
        self.sets_menu = SetsMenu(self)
        self.garage_menu = GarageMenu(self)

        # BUTTONS GAME

        button_sound = pg.mixer.Sound("audio/button_sound.mp3")
        self.close_button_game = Button(580, 360, "images/buttons/close_button_off.png", "images/buttons/close_button_on.png", button_sound, 0.25)
        self.back_button = Button(700, 360, "images/buttons/back_button_off.png", "images/buttons/back_button_on.png", button_sound, 0.25)

        # BACKGROUND

        self.bg_summer = Background("images/backgrounds/background_new.png")

        # CARS
        self.player_car_1 = Picture(750, 450, f'images/cars/opp{settings.car}.png', 1.1)
        self.enemy_car_1 = Picture(430, 100, "images/cars/opp1.png", 1.1)

        self.speed = 15

        # crash = pg.image.load('images/crash.png')

        # player_group = pg.sprite.Group()
        # vehicle_group = pg.sprite.Group()

        # player_group.add(self.player)



    def game_loop(self):
        P1 = Player(f'images/cars/opp{settings.car}.png', 750, 500)
        P1.set_speed(self.speed)
        E1 = Enemy("images/cars/opp1.png")
        E1.set_speed(self.speed)
        # enemies_list = pg.sprite.Group()
        # all_sprites_list = pg.sprite.Group()

        # enemies_list.add(E1)
        # all_sprites_list.add(P1)

        while self.playing:
            self.check_events()

            if self.game_state == "PAUSED":
                self.bg_summer.scroll(self.screen, 0)

                P1.set_speed(0)
                E1.set_speed(0)
                P1.move(self.screen)
                E1.move(self.screen)

                if self.close_button_game.draw(self.screen, False) and self.clicked:
                    self.playing = False
                    self.game_state = "GAME"
                if self.back_button.draw(self.screen, False) and self.clicked:
                    self.game_state = "GAME"
            else:
                self.bg_summer.scroll(self.screen, self.speed)

                P1.set_speed(self.speed)
                E1.set_speed(self.speed)
                P1.move(self.screen)
                E1.move(self.screen)

            self.window.blit(self.screen, (0, 0))
            pg.display.update()
            self.frame_per_second.tick(self.FPS)
            self.reset_keys()

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
                if event.key in [pg.K_a, pg.K_LEFT] and self.player_car_1.rect[0] != 450:
                    self.player_car_1.rect = self.player_car_1.rect.move([-300, 0])
                if event.key in [pg.K_d, pg.K_RIGHT] and self.player_car_1.rect[0] != 750:
                    self.player_car_1.rect = self.player_car_1.rect.move([300, 0])
                if event.key == pg.K_ESCAPE:
                    if self.game_state == "PAUSED":
                        self.game_state = "GAME"
                    else:
                        self.game_state = "PAUSED"

    def reset_keys(self):
        self.screen = pg.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def draw_text(self, x, y, text, size=30):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
