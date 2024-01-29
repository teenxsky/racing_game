from .Menu import *
import cv2
import numpy
from PIL import Image
import pygame.camera


class GarageMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

        self.player_stats = PlayerStats()

        self.garage_close_button = Button("Resources/Images/Buttons/close_button_off.png",
                                          "Resources/Images/Buttons/close_button_on.png", button_sound, 0.15)

        self.garage_back_button = Button("Resources/Images/Buttons/back_button_off.png",
                                         "Resources/Images/Buttons/back_button_on.png", button_sound, 0.15)
        self.garage_forward_button = Button("Resources/Images/Buttons/forward_button_off.png",
                                            "Resources/Images/Buttons/forward_button_on.png", button_sound, 0.15)

        self.license_icon = Button("Resources/Images/License/license_icon_off.png",
                                   "Resources/Images/License/license_icon_on.png", button_sound, 0.13)
        self.license_img = Picture("Resources/Images/License/license.png", 0.5)
        self.photo_button = Button("Resources/Images/Buttons/photo_button_off.png",
                                   "Resources/Images/Buttons/photo_button_on.png", button_sound, 0.07)

        self.logo_pic = Picture("Resources/Images/License/team_logo.png", scale=0.15)

        self.window_specs_1 = Picture("Resources/Images/Backgrounds/window_garage.png", 0.4)
        self.window_specs_2 = Picture("Resources/Images/Backgrounds/window_garage.png", 0.4)

        self.scroll_y_1 = 0
        self.scroll_x_2 = 0

        self.license = False

        self.camera_on = False

        self.bgs = []
        for file in sorted(os.listdir("Resources/Images/Backgrounds/bgs/")):
            if not file.startswith('.'):
                preview = os.listdir("Resources/Images/Backgrounds/bgs/" + file + "/")[1]
                try:
                    level_img = Picture("Resources/Images/Backgrounds/bgs/" + file + "/" + preview, (140, 100))
                    self.bgs.append((level_img, file))
                except pygame.error:
                    pass

        self.choose_button = Button("Resources/Images/Buttons/choose_button_off.png",
                                    "Resources/Images/Buttons/choose_button_on.png", button_sound, 0.1)
        self.buy_button = Button("Resources/Images/Buttons/buy_button_off.png",
                                 "Resources/Images/Buttons/buy_button_on.png",
                                 button_sound, 0.1)

        self.garage_bg, self.garage_bg_speed = load_bg("garage_bg")
        self.bg_sound = load_bg_sound("garage_bg")

        self.exit = False
        self.last_update = pg.time.get_ticks()

        self.sub_state = "GARAGE"
        self.block = False

    def display_menu(self):

        cars = []
        for car in settings.cars:
            cars.append((car["specs"], car["name"],
                         Picture(f'Resources/Images/cars/{car["name"]}.png', car["garage_size"])))

        curr_lvl_x = 860
        while self.game.menu_state == "GARAGE" and self.game.running:
            self.check_events()

            self.garage_bg.draw(self.game.screen, self.garage_bg_speed)

            if not self.bg_sound.num_channels:
                self.bg_sound.play(loops=-1, fade_ms=500)

            if self.license_icon.draw(self.game.screen, (1170, 80), self.block) and self.game.keys["MOUSE DOWN"]:
                self.sub_state = "LICENSE"

            self.player_stats.draw_coins(self.game.screen,
                                         (self.license_icon.rect.midleft[0] - 25, self.license_icon.rect.midleft[1]),
                                         position="midright")
            self.player_stats.draw_level(self.game.screen, (
                self.license_icon.rect.bottomright[0], self.license_icon.rect.bottomright[1] + 15), position="topleft")

            distance = 0
            for car in cars:
                car[2].draw(self.game.screen, (curr_lvl_x + distance, car[2].rect.center[1]))
                if curr_lvl_x + distance == 860:
                    self.show_specs(car, cars.index(car))
                distance += 700
            distance -= 700

            if self.game.keys["ENTER"]:
                self.player_stats.increase_score(100)

            if curr_lvl_x + 700 <= 860:
                if (self.garage_back_button.draw(self.game.screen, (530, 200), self.block) and self.game.keys[
                    "MOUSE DOWN"]) or (
                        self.game.keys["MOVE LEFT"]):
                    curr_lvl_x += 700

            if curr_lvl_x + distance - 700 >= 860:
                if (self.garage_forward_button.draw(self.game.screen, (530, 290), self.block) and self.game.keys[
                    "MOUSE DOWN"]) or (
                        self.game.keys["MOVE RIGHT"]):
                    curr_lvl_x -= 700

            if self.garage_close_button.draw(self.game.screen, (30, 30), self.block, position="topleft") and \
                    self.game.keys["MOUSE DOWN"]:
                # self.game.menu_state = "MENU"
                self.last_update = pg.time.get_ticks()
                self.exit = True
                self.game.transition = True

            self.show_menu_shop()

            self.check_input()
            if self.exit and delay(self.last_update):
                self.game.menu_state = "MENU"
                self.exit = False
            else:
                self.game.blit_screen()

        self.bg_sound.stop(fadeout=500)
        # pg.time.delay(500)

    def show_specs(self, car, car_index):
        specs, name, _ = car

        self.window_specs_1.draw(self.game.screen, (20, 120), position="topleft")

        bar_1 = pg.surface.Surface((380, 90)).convert_alpha()
        bar_1.fill(BROWN)
        bar_1_rect = bar_1.get_rect()
        bar_1_rect.topleft = (75, 185)

        distance = 0
        for spec in specs.keys():
            s_key = Text(spec + ": ", 20, color=BLUE)
            s_val = Text(str(specs[spec]["val"]), 20)

            s_key.draw(bar_1, (0, distance + self.scroll_y_1), position="topleft")

            if settings.cars[car_index]["own"]:
                if s_val.draw_as_button(bar_1, (s_key.rect.topright[0], distance + self.scroll_y_1), self.block,
                                        surface_topleft=bar_1_rect.topleft, position="topleft"):
                    if self.player_stats.show_cost(bar_1, settings.cars[car_index]["specs"][spec]["cost"],
                                                   surface_topleft=bar_1_rect.topleft) and self.game.keys["MOUSE DOWN"]:
                        if settings.cars[car_index]["specs"][spec]["val"] + settings.cars[car_index]["specs"][spec][
                                "d_val"] <= settings.cars[car_index]["specs"][spec]["max_val"]:
                            settings.cars[car_index]["specs"][spec]["val"] += settings.cars[car_index]["specs"][spec][
                                "d_val"]
                            self.player_stats.decrease_coins(settings.cars[car_index]["specs"][spec]["cost"])
                            settings.cars[car_index]["specs"][spec]["cost"] += settings.cars[car_index]["specs"][spec][
                                "d_cost"]
                if not settings.cars[car_index]["chosen"]:
                    if self.choose_button.draw(self.game.screen, (120, 300), self.block) and self.game.keys[
                            "MOUSE DOWN"]:
                        for car in settings.cars:
                            car["chosen"] = False
                        settings.cars[car_index]["chosen"] = True
            else:
                if self.buy_button.draw(self.game.screen, (400, 300), self.block):
                    if self.player_stats.show_cost(self.game.screen, settings.cars[car_index]["cost"]) and \
                            self.game.keys[
                                "MOUSE DOWN"]:
                        settings.cars[car_index]["own"] = True

            distance += 30

        pos = pg.mouse.get_pos()
        if bar_1_rect.collidepoint(pos) and self.scroll_y_1 + (self.game.keys["MOUSEWHEEL"] * 10) <= 0 \
                and (distance + self.scroll_y_1) + (self.game.keys["MOUSEWHEEL"] * 10) >= bar_1_rect.height:
            self.scroll_y_1 += self.game.keys["MOUSEWHEEL"] * 10

        self.game.screen.blit(bar_1, bar_1_rect)

        car_name = Text(" ".join(name.split("_")), 27)
        car_name.draw(self.game.screen, (260, 165))

    def show_menu_shop(self):
        self.window_specs_2.draw(self.game.screen, (20, 400), position="topleft")

        bar_2 = pg.surface.Surface((380, 120)).convert_alpha()
        bar_2.fill(BROWN)
        bar_2_rect = bar_2.get_rect()
        bar_2_rect.topleft = (75, 460)

        car_name = Text("BG SHOP", 27)
        car_name.draw(self.game.screen, (260, 445))

        distance = 0
        for bg in self.bgs:
            if bg[0].draw(bar_2, (self.scroll_x_2 + distance, bar_2_rect.height // 2), self.block,
                          surface_topleft=bar_2_rect.topleft, position="midleft"):
                if self.player_stats.show_cost(bar_2, 500, surface_topleft=bar_2_rect.topleft) and self.game.keys[
                        "MOUSE DOWN"]:
                    settings.current_bg["menu_bg"] = bg[1]
                    self.player_stats.decrease_coins(500)
                    self.game.main_menu.menu_bg, self.game.main_menu.menu_bg_speed = load_bg("menu_bg")
                    self.game.main_menu.bg_sound = load_bg_sound("menu_bg")
            distance += 180

        pos = pg.mouse.get_pos()
        if bar_2_rect.collidepoint(pos) and self.scroll_x_2 + (self.game.keys["MOUSEWHEEL"] * 10) <= 0 \
                and (distance + self.scroll_x_2) + (self.game.keys["MOUSEWHEEL"] * 10) >= bar_2_rect.width:
            self.scroll_x_2 += self.game.keys["MOUSEWHEEL"] * 10

        self.game.screen.blit(bar_2, bar_2_rect)

    def display_license(self):
        bar = pg.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA).convert_alpha()
        bar.fill((0, 0, 0, 150))
        self.game.screen.blit(bar, (0, 0))

        text_player_statistics = Text("PLAYER STATISTICS", 45)
        distance = 80
        for key in settings.player_stats.keys():
            if key == "time_in_game":
                text = self.player_stats.get_time_in_game()
            else:
                text = settings.player_stats[key]
            if key != "photo":
                curr_text = Text(f'{" ".join(key.split("_"))}: {text}', 30)
                curr_text.draw(self.game.screen, (
                    text_player_statistics.rect.midleft[0], text_player_statistics.rect.midleft[1] + distance),
                               position="midleft")
                distance += 40

        i = 1
        license_name = Text(settings.player_stats["name"].upper(), 21, font="Resources/Fonts/pixelscript.ttf",
                            color=BLACK)
        while license_name.rect.width >= 271:
            license_name = Text(settings.player_stats["name"].upper(), 21 - i, font="Resources/Fonts/pixelscript.ttf",
                                color=BLACK)
            i += 1

        license_level = Text(str(settings.player_stats["level"]), 21, font="Resources/Fonts/pixelscript.ttf")

        license_name_mini_0 = Text("NAME: ", 23)
        license_name_mini_1 = Text(str(settings.player_stats["name"]), 23)

        current_car = ""
        for car in settings.cars:
            if car["chosen"]:
                current_car = " ".join(car["name"].split("_"))
        license_car = Text("CAR: " + current_car, 23)

        license_wins = Text("WINS: " + str(settings.player_stats["wins"]), 23)

        text_player_statistics.draw(self.game.screen, (660, 130), position="midleft")
        self.license_img.draw(self.game.screen, (330, 360))
        license_name.draw(self.game.screen, (94, 443), position="midleft")
        license_level.draw(self.game.screen, (129, 323))
        license_car.draw(self.game.screen, (200, 325), position="midleft")
        license_wins.draw(self.game.screen, (200, 355), position="midleft")

        license_name_mini_0.draw(self.game.screen, (200, 295), position="midleft")
        screen_without_name = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        screen_without_name.blit(self.game.screen, (0, 0))

        if license_name_mini_1.draw_as_button(self.game.screen, (license_name_mini_0.rect.bottomright[0], 295),
                                              position="midleft"):
            if self.player_stats.show_cost(self.game.screen, 100) and self.game.keys["MOUSE DOWN"]:
                self.player_stats.decrease_coins(100)
                license_name_mini_1.typing(screen_without_name, self.game, set_left=True)
                settings.player_stats["name"] = license_name_mini_1.string

        photo = None
        for file in sorted(os.listdir("Resources/Images/License/")):
            if file == "photo_" + str(settings.player_stats["photo"]) + ".png":
                photo = Picture("Resources/Images/License/" + file, (150, 150))
        photo.draw(self.game.screen, (495, 430))

        self.logo_pic.draw(self.game.screen, (543, 483))

        if self.photo_button.draw(self.game.screen, (554, 490)):
            if self.player_stats.show_cost(self.game.screen, 200) and self.game.keys["MOUSE DOWN"]:
                self.camera_on = True

        if self.camera_on:
            self.make_photo()

        if self.game.keys["BACK"]:
            self.sub_state = "GARAGE"

    def make_photo(self):
        bar = pg.surface.Surface((470, 220), pg.SRCALPHA)
        bar = bar.convert_alpha()
        bar.fill((0, 0, 0, 200))

        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FPS, 60)

        success, frame = cam.read()
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = numpy.fliplr(frame)
        # frame = numpy.rot90(frame)

        if self.game.keys["BACK"]:
            img_name = "Resources/Images/License/opencv_frame.png"
            cv2.imwrite(img_name, frame)

            image1 = Image.open("Resources/Images/License/license.png")
            image2 = Image.open("Resources/Images/License/opencv_frame.png")
            # image3 = Image.open("Resources/Images/License/team_logo.png")
            image2.crop((500, 200, 600, 300))
            image2 = image2.resize((300, 300))
            image1.paste(image2, (800, 300))
            # image3.resize((100, 100))
            # image1.paste(image3, (850, 200))
            image1.save("Resources/Images/License/merged_image.png", "PNG")
            self.camera_on = False

        frame = pg.surfarray.make_surface(frame)
        bar.blit(frame, (-500, 0))

    def check_input(self):
        self.block = self.sub_state == "LICENSE"

        if self.sub_state == "LICENSE":
            self.display_license()
