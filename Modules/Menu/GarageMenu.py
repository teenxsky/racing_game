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
                    self.bgs.append({"image": level_img, "file": file})
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
            car_info = {"specs": car["specs"],
                        "name": car["name"],
                        "garage_car_y": car["garage_car_y"],
                        "image": Picture(f'Resources/Images/cars/{car["name"]}.png', car["garage_size"])}
            cars.append(car_info)

        car_x_center = 430
        curr_lvl_x = car_x_center
        while self.game.menu_state == "GARAGE" and self.game.running:
            self.check_events()

            self.garage_bg.draw(self.game.screen, self.garage_bg_speed)

            if not self.bg_sound.num_channels:
                self.bg_sound.play(loops=-1, fade_ms=500)

            if self.license_icon.draw(self.game.screen, (1260, 20), self.block, position="topright") and self.game.keys["MOUSE DOWN"]:
                self.sub_state = "LICENSE"

            self.player_stats.draw_coins(self.game.screen,
                                         (self.license_icon.rect.midleft[0] - 20, self.license_icon.rect.midleft[1]),
                                         position="midright")
            self.player_stats.draw_level(self.game.screen, (
                self.license_icon.rect.bottomright[0], self.license_icon.rect.bottomright[1] + 20), position="topright")

            specs_to_show = None
            distance, i = 0, 0
            for car in cars:
                if curr_lvl_x + distance == car_x_center:
                    specs_to_show = car, i
                car["image"].draw(self.game.screen, (curr_lvl_x + distance, car["garage_car_y"]))
                i += 1
                distance += 700
            distance -= 700

            self.show_specs(*specs_to_show)

            if self.game.keys["ENTER"]:
                self.player_stats.increase_score(100)

            if curr_lvl_x + 700 <= car_x_center:
                if (self.garage_back_button.draw(self.game.screen, (20, 700), self.block, position="bottomleft") and self.game.keys[
                    "MOUSE DOWN"]) or (
                        self.game.keys["MOVE LEFT"]):
                    curr_lvl_x += 700

            if curr_lvl_x + distance - 700 >= car_x_center:
                if (self.garage_forward_button.draw(self.game.screen, (725, 700), self.block, position="bottomleft") and self.game.keys[
                    "MOUSE DOWN"]) or (
                        self.game.keys["MOVE RIGHT"]):
                    curr_lvl_x -= 700

            if self.garage_close_button.draw(self.game.screen, (20, 20), self.block, position="topleft") and \
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
        specs = car["specs"]
        name = car["name"]

        self.window_specs_1.draw(self.game.screen, (1260, 195), position="topright")

        window_x, window_y = self.window_specs_1.rect.topleft

        bar_1 = pg.surface.Surface((380, 90)).convert_alpha()
        bar_1.fill(BROWN)
        bar_1_rect = bar_1.get_rect()
        bar_1_rect.topleft = (window_x + 55, window_y + 65)

        cost_bar, afford = None, None

        distance = 0
        for spec in specs.keys():
            s_key = Text(spec + ": ", 20, color=BLUE)
            s_val = Text(str(specs[spec]["val"]), 20)

            s_key.draw(bar_1, (0, distance + self.scroll_y_1), position="topleft")

            if settings.cars[car_index]["own"]:
                if s_val.draw_as_button(bar_1, (s_key.rect.topright[0], distance + self.scroll_y_1), self.block,
                                        surface_topleft=bar_1_rect.topleft, position="topleft"):

                    cost_bar, afford = self.player_stats.get_cost_bar(settings.cars[car_index]["specs"][spec]["cost"])

                    if afford and self.game.keys["MOUSE DOWN"]:
                        if settings.cars[car_index]["specs"][spec]["val"] + settings.cars[car_index]["specs"][spec][
                                "d_val"] <= settings.cars[car_index]["specs"][spec]["max_val"]:
                            settings.cars[car_index]["specs"][spec]["val"] += settings.cars[car_index]["specs"][spec][
                                "d_val"]
                            self.player_stats.coins -= settings.cars[car_index]["specs"][spec]["cost"]
                            settings.cars[car_index]["specs"][spec]["cost"] += settings.cars[car_index]["specs"][spec][
                                "d_cost"]
                if not settings.cars[car_index]["chosen"]:
                    if self.choose_button.draw(self.game.screen, (window_x + 100, window_y + 180), self.block) and self.game.keys[
                            "MOUSE DOWN"]:
                        for car in settings.cars:
                            car["chosen"] = False
                        settings.cars[car_index]["chosen"] = True
            else:
                if self.buy_button.draw(self.game.screen, (window_x + 380, window_y + 180), self.block):
                    cost_bar, afford = self.player_stats.get_cost_bar(settings.cars[car_index]["cost"])
                    if afford and self.game.keys["MOUSE DOWN"]:
                        settings.cars[car_index]["own"] = True

            distance += 30

        pos = pg.mouse.get_pos()
        if bar_1_rect.collidepoint(pos) and self.scroll_y_1 + (self.game.keys["MOUSEWHEEL"] * 10) <= 0 \
                and (distance + self.scroll_y_1) + (self.game.keys["MOUSEWHEEL"] * 10) >= bar_1_rect.height:
            self.scroll_y_1 += self.game.keys["MOUSEWHEEL"] * 10

        self.game.screen.blit(bar_1, bar_1_rect)
        if cost_bar:
            self.game.screen.blit(cost_bar[0], cost_bar[1])

        car_name = Text(" ".join(name.split("_")), 27)
        car_name.draw(self.game.screen, (window_x + 240, window_y + 45))

    def show_menu_shop(self):
        self.window_specs_2.draw(self.game.screen, (1260, 455), position="topright")

        window_x, window_y = self.window_specs_2.rect.topleft

        bar_2 = pg.surface.Surface((380, 120)).convert_alpha()
        bar_2.fill(BROWN)
        bar_2_rect = bar_2.get_rect()
        bar_2_rect.topleft = (window_x + 55, window_y + 60)

        shop_name = Text("BG SHOP", 27)
        shop_name.draw(self.game.screen, (window_x + 240, window_y + 45))

        cost_bar, afford = None, None

        distance = 0
        for bg in self.bgs:
            if bg["image"].draw(bar_2, (self.scroll_x_2 + distance, bar_2_rect.height // 2), self.block,
                          surface_topleft=bar_2_rect.topleft, position="midleft"):

                cost_bar, afford = self.player_stats.get_cost_bar(500)

                if afford and self.game.keys["MOUSE DOWN"]:
                    settings.current_bg["menu_bg"] = bg["file"]
                    self.player_stats.coins -= 500
                    self.game.main_menu.menu_bg, self.game.main_menu.menu_bg_speed = load_bg("menu_bg")
                    self.game.main_menu.bg_sound = load_bg_sound("menu_bg")
            distance += 180

        pos = pg.mouse.get_pos()
        if bar_2_rect.collidepoint(pos) and self.scroll_x_2 + (self.game.keys["MOUSEWHEEL"] * 10) <= 0 \
                and (distance + self.scroll_x_2) + (self.game.keys["MOUSEWHEEL"] * 10) >= bar_2_rect.width:
            self.scroll_x_2 += self.game.keys["MOUSEWHEEL"] * 10

        self.game.screen.blit(bar_2, bar_2_rect)
        if cost_bar:
            self.game.screen.blit(cost_bar[0], cost_bar[1])

    def display_license(self):
        bar = pg.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA).convert_alpha()
        bar.fill((0, 0, 0, 150))
        self.game.screen.blit(bar, (0, 0))

        text_player_statistics = Text("PLAYER STATISTICS", 45)
        text_player_statistics.draw(self.game.screen, (660, 130), position="midleft")

        distance = 80
        for key in settings.player_stats.keys():
            if key == "time_in_game":
                text = self.player_stats.time_in_game
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


        self.license_img.draw(self.game.screen, (330, 360))
        license_name.draw(self.game.screen, (94, 443), position="midleft")
        license_level.draw(self.game.screen, (129, 323))
        license_car.draw(self.game.screen, (200, 325), position="midleft")
        license_wins.draw(self.game.screen, (200, 355), position="midleft")

        license_name_mini_0.draw(self.game.screen, (200, 295), position="midleft")
        screen_without_name = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        screen_without_name.blit(self.game.screen, (0, 0))

        cost_bar, afford = None, None

        if license_name_mini_1.draw_as_button(self.game.screen, (license_name_mini_0.rect.bottomright[0], 295),
                                              position="midleft"):

            cost_bar, afford = self.player_stats.get_cost_bar(100)

            if afford and self.game.keys["MOUSE DOWN"]:
                self.player_stats.coins -= 100
                license_name_mini_1.typing(screen_without_name, self.game, set_left=True)
                settings.player_stats["name"] = license_name_mini_1.string

        photo = None
        for file in sorted(os.listdir("Resources/Images/License/")):
            if file == "photo_" + str(settings.player_stats["photo"]) + ".png":
                photo = Picture("Resources/Images/License/" + file, (150, 150))
        photo.draw(self.game.screen, (495, 430))

        self.logo_pic.draw(self.game.screen, (543, 483))

        if self.photo_button.draw(self.game.screen, (554, 490)):

            cost_bar, afford = self.player_stats.get_cost_bar(10000)

            if afford and self.game.keys["MOUSE DOWN"]:
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
