import pygame as pg
from menu import MainMenu
from objects import Button, Picture

pg.init()

class Game:
    def __init__(self):
        pg.init()
        self.running, self.playing = True, False
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 720
        self.clicked = False
        self.screen = pg.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.window = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.FPS = 60
        self.font_name = "fonts/pixfont.ttf"
        self.frame_per_second = pg.time.Clock()
        self.speed = 5

        #MENU
        self.main_menu = MainMenu(self)
        button_sound = pg.mixer.Sound("audio/button_sound.mp3")

        title_image = pg.image.load("images/title_name.png")
        self.title_picture = Picture(400, 15, title_image, 0.5)

        #CARS
        player_car_1 = pg.image.load("images/cars/player_car_1.png").convert_alpha()
        self.player_car_1 = Picture(750, 450, player_car_1, 1.1)

        opp_car_1 = pg.image.load("images/cars/opp1.png").convert_alpha()
        self.opp_car_1 = Picture(450, 100, opp_car_1, 1.1)

        #BACKGROUNDS
        game_background_summer = pg.image.load("images/backgrounds/sumer_road.png").convert_alpha()
        self.game_background_summer = Picture(240, 0, game_background_summer)
        self.game_background_summer.resize(800, self.SCREEN_HEIGHT)

        summer_details = pg.image.load("images/backgrounds/summer_details.png").convert_alpha()
        self.summer_details = Picture(0, 0, summer_details)
        self.summer_details.resize(240, 72)
        self.summer_details_coordinates = [[0, 0], [0, 240], [0, 480], [1000, 0], [1000, 240], [1000, 480]]

        #BUTTONS
        start_but_off = pg.image.load("images/buttons/start_button_off.png").convert_alpha()
        start_but_on = pg.image.load("images/buttons/start_button_on.png").convert_alpha()
        self.start_button = Button(100, 70, start_but_off, start_but_on, button_sound, 0.3)

        garage_but_off = pg.image.load("images/buttons/garage_button_off.png").convert_alpha()
        garage_but_on = pg.image.load("images/buttons/garage_button_on.png").convert_alpha()
        self.garage_button = Button(100, 190, garage_but_off, garage_but_on, button_sound, 0.3)

        music_but_off = pg.image.load("images/buttons/music_button_off.png").convert_alpha()
        music_but_on = pg.image.load("images/buttons/music_button_on.png").convert_alpha()
        self.music_button = Button(100, 310, music_but_off, music_but_on, button_sound, 0.3)

        sets_but_off = pg.image.load("images/buttons/settings_button_off.png").convert_alpha()
        sets_but_on = pg.image.load("images/buttons/settings_button_on.png").convert_alpha()
        self.sets_button = Button(100, 430, sets_but_off, sets_but_on, button_sound, 0.3)

        quit_but_off = pg.image.load("images/buttons/quit_button_off.png").convert_alpha()
        quit_but_on = pg.image.load("images/buttons/quit_button_on.png").convert_alpha()
        self.quit_button = Button(100, 550, quit_but_off, quit_but_on, button_sound, 0.3)

        close_but_off = pg.image.load("images/buttons/close_button_off.png").convert_alpha()
        close_but_on = pg.image.load("images/buttons/close_button_on.png").convert_alpha()
        self.close_button = Button(550, 300, close_but_off, close_but_on, button_sound, 0.25)

        back_but_off = pg.image.load("images/buttons/back_button_off.png").convert_alpha()
        back_but_on = pg.image.load("images/buttons/back_button_on.png").convert_alpha()
        self.back_button = Button(670, 300, back_but_off, back_but_on, button_sound, 0.25)

        self.game_state = "GAME"

    def game_loop(self):
        pg.display.set_caption("gameloop")
        self.game_state = "GAME"

        while self.playing:
            self.check_events()
            self.window.fill((66, 173, 55))

            self.window.blit(self.game_background_summer.image, self.game_background_summer.rect)
            self.window.blit(self.game_background_summer.image, (self.game_background_summer.rect[0], -self.SCREEN_HEIGHT + self.game_background_summer.rect[1]))
            if self.game_background_summer.rect[1] == self.SCREEN_HEIGHT:
                self.game_background_summer.rect.topleft = (240, 0)
            self.game_background_summer.rect = self.game_background_summer.rect.move([0, self.speed])

            self.window.blit(self.summer_details.image, self.summer_details_coordinates[0])
            self.window.blit(self.summer_details.image, (self.summer_details_coordinates[0][0], -self.SCREEN_HEIGHT + self.summer_details_coordinates[0][1]))
            if self.summer_details_coordinates[0][1] == self.SCREEN_HEIGHT:
                self.summer_details_coordinates[0] = [0, 0]
            self.summer_details_coordinates[0][1] += self.speed

            self.window.blit(self.summer_details.image, self.summer_details_coordinates[1])
            self.window.blit(self.summer_details.image, (self.summer_details_coordinates[1][0], -self.SCREEN_HEIGHT + self.summer_details_coordinates[1][1]))
            if self.summer_details_coordinates[1][1] == self.SCREEN_HEIGHT + 240:
                self.summer_details_coordinates[1] = [0, 240]
            self.summer_details_coordinates[1][1] += self.speed

            self.window.blit(self.summer_details.image, self.summer_details_coordinates[2])
            self.window.blit(self.summer_details.image, (self.summer_details_coordinates[2][0], -self.SCREEN_HEIGHT + self.summer_details_coordinates[2][1]))
            if self.summer_details_coordinates[2][1] == self.SCREEN_HEIGHT + 480:
                self.summer_details_coordinates[2] = [0, 480]
            self.summer_details_coordinates[2][1] += self.speed

            self.window.blit(self.summer_details.image, self.summer_details_coordinates[3])
            self.window.blit(self.summer_details.image, (self.summer_details_coordinates[3][0], -self.SCREEN_HEIGHT + self.summer_details_coordinates[3][1]))
            if self.summer_details_coordinates[3][1] == self.SCREEN_HEIGHT:
                self.summer_details_coordinates[3] = [1000, 0]
            self.summer_details_coordinates[3][1] += self.speed

            self.window.blit(self.summer_details.image, self.summer_details_coordinates[4])
            self.window.blit(self.summer_details.image, (self.summer_details_coordinates[4][0], -self.SCREEN_HEIGHT + self.summer_details_coordinates[4][1]))
            if self.summer_details_coordinates[4][1] == self.SCREEN_HEIGHT + 240:
                self.summer_details_coordinates[4] = [1000, 240]
            self.summer_details_coordinates[4][1] += self.speed

            self.window.blit(self.summer_details.image, self.summer_details_coordinates[5])
            self.window.blit(self.summer_details.image, (self.summer_details_coordinates[5][0], -self.SCREEN_HEIGHT + self.summer_details_coordinates[5][1]))
            if self.summer_details_coordinates[5][1] == self.SCREEN_HEIGHT + 480:
                self.summer_details_coordinates[5] = [1000, 480]
            self.summer_details_coordinates[5][1] += self.speed





            self.window.blit(self.player_car_1.image, self.player_car_1.rect)
            self.window.blit(self.opp_car_1.image, self.opp_car_1.rect)

            if self.game_state == "PAUSE":
                if self.close_button.draw(self.window):
                    self.playing = False
                if self.back_button.draw(self.window):
                    self.game_state = "GAME"

            pg.display.update()
            self.frame_per_second.tick(self.FPS)
            self.reset_keys()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running, self.playing = False, False
                self.main_menu.run_display = False
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_a, pg.K_LEFT] and self.player_car_1.rect[0] != 450:
                    self.player_car_1.rect = self.player_car_1.rect.move([-300, 0])
                if event.key in [pg.K_d, pg.K_RIGHT] and self.player_car_1.rect[0] != 750:
                    self.player_car_1.rect = self.player_car_1.rect.move([300, 0])
                if event.key == pg.K_ESCAPE:
                    if self.game_state == "PAUSE":
                        self.game_state = "GAME"
                    else:
                        self.game_state = "PAUSE"

    def reset_keys(self):
        self.screen = pg.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def draw_text(self, text, size, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, False, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

class moving:
    def __init__(self, rotation_vel):
        self.rotation_vel = rotation_vel
        self.angle = 0
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
